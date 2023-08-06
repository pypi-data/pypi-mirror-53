import warnings
from typing import Iterable, Optional, Union

from starfish.core.imagestack.imagestack import ImageStack
from starfish.core.types import Axes
from ._base import FilterAlgorithm


class MaxProject(FilterAlgorithm):
    """
    Creates a maximum projection over one or more axis of the image tensor

    .. deprecated:: 0.1.2
        Use `Filter.Reduce(func='max')` instead.

    Parameters
    ----------
    dims : Axes
        one or more Axes to project over

    See Also
    --------
    starfish.types.Axes

    """

    def __init__(self, dims: Iterable[Union[Axes, str]]) -> None:

        warnings.warn(
            "Filter.MaxProject is being deprecated in favor of Filter.Reduce(func='max')",
            DeprecationWarning,
        )
        self.dims = dims

    _DEFAULT_TESTING_PARAMETERS = {"dims": 'r'}

    def run(
            self,
            stack: ImageStack,
            in_place: bool = False,
            verbose: bool = False,
            n_processes: Optional[int] = None,
            *args,
    ) -> Optional[ImageStack]:
        """Perform filtering of an image stack

        Parameters
        ----------
        stack : ImageStack
            Stack to be filtered.
        in_place : bool
            if True, process ImageStack in-place, otherwise return a new stack
        verbose : bool
            if True, report on filtering progress (default = False)
        n_processes : Optional[int]
            Number of parallel processes to devote to calculating the filter

        Returns
        -------
        ImageStack :
            If in-place is False, return the results of filter as a new stack. Otherwise return the
            original stack.

        """
        return stack.max_proj(*tuple(Axes(dim) for dim in self.dims))
