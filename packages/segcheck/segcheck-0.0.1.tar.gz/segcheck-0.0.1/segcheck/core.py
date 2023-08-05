"""segcheck helps to find gaps and overlaps in segments"""

from itertools import tee
from .exceptions import InvalidSegmentError


def gaps(segments: list) -> list:
    """Returns gaps between segments.

        Args:
            segments (list): List of segments.

        Returns:
            list: List of intervals where no segment is present.

        Example:
            >>> from segcheck.core import gaps
            >>> gaps([[1, 2], [3, 4]])
            [[2, 3]]

        Raises:
            InvalidSegmentError: At least one segment within the segments is invalid."""

    _validate(segments)

    gap_list = []

    intervals = _intersect(segments)

    for interval in intervals:

        overlap_count = len(
            [
                segment
                for segment in segments
                if interval[0] >= segment[0] and interval[1] <= segment[1]
            ]
        )

        if overlap_count == 0:
            gap_list.append(interval)

    return gap_list


def overlaps(segments: list) -> list:
    """Returns overlaps between the segments.

        Args:
            segments (list): List of segments.

        Returns:
            list: List of intervals where multiple segments are present.

        Example:
            >>> from segcheck.core import overlaps
            >>> overlaps([[1, 3], [2, 4]])
            [[2, 3]]

        Raises:
            InvalidSegmentError: At least one segment within the segments is invalid."""

    _validate(segments)

    overlap_list = []

    intervals = _intersect(segments)

    for interval in intervals:

        overlap_count = len(
            [
                segment
                for segment in segments
                if interval[0] >= segment[0] and interval[1] <= segment[1]
            ]
        )

        if overlap_count > 1:
            overlap_list.append(interval)

    return overlap_list


def has_gaps(segments: list) -> bool:
    """Returns True if the segments have gaps.

        Args:
            segments (list): List of segments.

        Returns:
            bool: True if the segments contains gaps, False otherwise.

        Examples:
            >>> from segcheck.core import has_gaps
            >>> has_gaps([[1, 2], [3, 4]])
            True

            >>> from segcheck.core import has_gaps
            >>> has_gaps([[1, 2], [2, 3]])
            False

        Raises:
            InvalidSegmentError: At least one segment within the segments is invalid."""

    if gaps(segments):
        return True
    return False


def has_overlaps(segments: list) -> bool:
    """Returns True if the segments have overlaps.

        Args:
            segments (list): List of segments.

        Returns:
            bool: True if the segments contains overlaps, False otherwise.

        Examples:
            >>> from segcheck.core import has_overlaps
            >>> has_overlaps([[1, 3], [2, 4]])
            True

            >>> from segcheck.core import has_overlaps
            >>> has_overlaps([[1, 2], [2, 3]])
            False

        Raises:
            InvalidSegmentError: At least one segment within the segments is invalid."""

    if overlaps(segments):
        return True
    return False


def _validate(segments: list):
    """Checks if the begin of a segment is smaller than its end."""
    for segment in segments:
        if segment[0] >= segment[1]:
            raise InvalidSegmentError(
                "Segment begin ({}) must be smaller than segment end ({}).".format(
                    segment[0], segment[1]
                )
            )


def _intersect(segments: list) -> list:
    """Intersect all segments with each other and return distinct intervals."""
    segments_beg = [beg[0] for beg in segments]
    segments_end = [end[1] for end in segments]

    segment_borders = list(set(segments_beg + segments_end))

    segment_borders.sort()

    return _pairwise(segment_borders)


def _pairwise(iterable: list) -> list:
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    val_a, val_b = tee(iterable)
    next(val_b, None)
    return [list(pair) for pair in zip(val_a, val_b)]