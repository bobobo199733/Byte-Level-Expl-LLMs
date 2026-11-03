def merge_intervals(intervals):
    """
    Merge overlapping intervals.

    Args:
        intervals (list[tuple[int, int]]): List of intervals in the form [(start, end), ...]

    Returns:
        list[tuple[int, int]]: Merged intervals
    """
    intervals.sort(key=lambda x: x[0])
    merged = []
    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], interval[1]))
    return merged