def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for current in intervals[1:]:
        last_merged_end = merged[-1][1]
        if current[0] <= last_merged_end:
            merged[-1][1] = max(last_merged_end, current[1])
        else:
            merged.append(current)
    return merged