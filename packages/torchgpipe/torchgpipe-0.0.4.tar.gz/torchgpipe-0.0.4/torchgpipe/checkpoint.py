"""Checkpointing with preceding recomputation.

PyTorch already provides the official checkpointing utilities in
:mod:`torch.utils.checkpoint`. The official checkpointing combines
recomputation and recursive backpropagation into one autograd function named
``CheckpointFunction``. Hence, the recomputation can be started only when the
gradients arrive to the function. In GPipe, the recomputation needs to precede
the gradient arrival to minimize the GPU idle time.

We solve this problem by introducing separate autograd functions named
:class:`Recompute` and :class:`Checkpoint`. Each function represents
recomputation and recursive backpropagation, respectively. We can manipulate
the control flow in aspect of both the autograd engine and CUDA with a pair of
the functions.

Specifically, we place CUDA stream synchronization between :class:`Recompute`
and :class:`Checkpoint` to delay only :class:`Checkpoint` until the gradient is
copied entirely.

"""
from collections import deque
from contextlib import contextmanager
import threading
from typing import Any, Callable, Deque, Generator, List, Optional, Tuple, Union

import torch
from torch import Tensor
import torch.autograd

from torchgpipe.dependency import fork, join
from torchgpipe.microbatch import Batch
from torchgpipe.phony import get_phony

__all__ = ['is_recomputing']


Tensors = Tuple[Tensor, ...]
TensorOrTensors = Union[Tensor, Tensors]
Function = Callable[[TensorOrTensors], TensorOrTensors]


def checkpoint(function: Function, input: TensorOrTensors) -> TensorOrTensors:
    """Makes a checkpoint with a simple interface like
    :func:`torch.utils.checkpoint.checkpoint`. It's only used to test or debug
    :class:`Checkpoint` and :class:`Recompute` without boilerplate.
    """
    batch = Batch(input)

    chk = Checkpointing(function, batch)
    batch = chk.checkpoint()
    chk.recompute(batch)

    return batch.tensor_or_tensors


class Checkpointing:
    """Generates a pair of :class:`Checkpoint` and :class:`Recompute`."""

    def __init__(self, function: Function, batch: Batch) -> None:
        self.function = function
        self.batch = batch
        self.recomputed: Deque[Tuple[TensorOrTensors, Tensors]] = deque(maxlen=1)

    def checkpoint(self) -> Batch:
        """Returns a batch applied by :class:`Checkpoint`."""
        input_atomic = self.batch.atomic
        input = tuple(self.batch)

        # Use a phony which requires grad to ensure that Checkpoint can be
        # tracked by the autograd engine even when none of the input tensors
        # require grad.
        phony = get_phony(self.batch[0].device, requires_grad=True)

        output = Checkpoint.apply(phony, self.recomputed, self.function, input_atomic, *input)
        return Batch(output)

    def recompute(self, batch: Batch) -> None:
        """Applies :class:`Recompute` to the batch in place."""
        input_atomic = self.batch.atomic
        input = tuple(self.batch)

        # batch[0] is always requiring grad, because it has been passed
        # checkpoint with a phony requiring grad.
        batch[0], phony = fork(batch[0])
        phony = Recompute.apply(phony, self.recomputed, self.function, input_atomic, *input)
        batch[0] = join(batch[0], phony)


_local = threading.local()


def is_recomputing() -> bool:
    """Whether if the current thread is under checkpoint recomputation.

    Returns:
        bool: ``True`` if it's under checkpoint recomputation.

    .. seealso:: :ref:`Detecting Recomputation`

    """
    return getattr(_local, 'is_recomputing', False)


@contextmanager
def enable_recomputing() -> Generator[None, None, None]:
    """Makes :func:`is_recomputing` return ``True`` within a context."""
    orig = is_recomputing()
    _local.is_recomputing = True
    try:
        yield
    finally:
        _local.is_recomputing = orig


class Context:
    """The common interface between the :class:`Checkpoint` and
    :class:`Recompute` context.
    """
    recomputed: Deque[Tuple[TensorOrTensors, Tensors]]

    # NOTE(sublee): 'function' cannot be annotated with 'Function' because mypy
    # infers this attribute as an instance method. That's why this is annotated
    # with 'Any' instead.
    # See: https://github.com/python/mypy/issues/708.
    function: Any

    input_atomic: bool

    saved_tensors: Tuple[Tensor, ...]

    def save_for_backward(self, *tensors: Tensor) -> None:  # pragma: no cover
        pass


class Checkpoint(torch.autograd.Function):
    @staticmethod
    def forward(ctx: Context,  # type: ignore
                phony: Tensor,
                recomputed: Deque[Tuple[TensorOrTensors, Tensors]],
                function: Function,
                input_atomic: bool,
                *input: Tensor,
                ) -> TensorOrTensors:
        ctx.recomputed = recomputed

        ctx.function = function
        ctx.input_atomic = input_atomic
        ctx.save_for_backward(*input)

        with torch.no_grad():
            output = function(input[0] if input_atomic else input)

        return output

    @staticmethod
    def backward(ctx: Context,
                 *grad_output: Tensor,
                 ) -> Tuple[Optional[Tensor], ...]:  # pragma: no cover
        output, input_leaf = ctx.recomputed.pop()

        if isinstance(output, tuple):
            tensors = output
        else:
            tensors = (output,)
        if any(y.requires_grad for y in tensors):
            torch.autograd.backward(tensors, grad_output)

        grad_input: List[Optional[Tensor]] = [None, None, None, None]
        grad_input.extend(x.grad for x in input_leaf)
        return tuple(grad_input)


class Recompute(torch.autograd.Function):
    @staticmethod
    def forward(ctx: Context,  # type: ignore
                phony: Tensor,
                recomputed: Deque[Tuple[TensorOrTensors, Tensors]],
                function: Function,
                input_atomic: bool,
                *input: Tensor,
                ) -> Tensor:
        ctx.recomputed = recomputed

        ctx.function = function
        ctx.input_atomic = input_atomic
        ctx.save_for_backward(*input)

        return phony

    @staticmethod
    def backward(ctx: Context, *grad_output: Tensor) -> Tuple[None, ...]:  # pragma: no cover
        input = ctx.saved_tensors
        input_leaf = tuple(x.detach().requires_grad_(x.requires_grad) for x in input)

        with torch.enable_grad(), enable_recomputing():
            output = ctx.function(input_leaf[0] if ctx.input_atomic else input_leaf)

        ctx.recomputed.append((output, input_leaf))

        return (None,) * (len(ctx.saved_tensors) + 4)
