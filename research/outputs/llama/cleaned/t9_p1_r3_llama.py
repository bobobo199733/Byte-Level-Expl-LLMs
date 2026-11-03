def merge_intervals(intervals):
    """
    Merges overlapping intervals in a given list of intervals.

    Args:
        intervals (list): A list of intervals where each interval is a list of two integers.

    Returns:
        list: A list of merged intervals.
    """
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for current in intervals[1:]:
        last_merged = merged[-1]
        if current[0] <= last_merged[1]:
            last_merged[1] = max(last_merged[1], current[1])
        else:
            merged.append(current)
    return merged