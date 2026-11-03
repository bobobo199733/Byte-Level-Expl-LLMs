def merge_intervals(intervals):
    """
    Merge all overlapping intervals in the given list of intervals.

    Args:
        intervals (list): A list of intervals, where each interval is [start, end].

    Returns:
        list: The merged intervals as a list of lists.
    """
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged_intervals = [intervals[0]]
    for current_interval in intervals[1:]:
        last_merged_interval = merged_intervals[-1]
        if current_interval[0] <= last_merged_interval[1]:
            merged_intervals[-1][1] = max(last_merged_interval[1], current_interval[1])
        else:
            merged_intervals.append(current_interval)
    return merged_intervals