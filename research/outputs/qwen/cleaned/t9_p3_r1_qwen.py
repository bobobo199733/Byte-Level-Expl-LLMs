def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for current_interval in intervals[1:]:
        last_merged_interval = merged[-1]
        if current_interval[0] <= last_merged_interval[1]:
            merged[-1] = [last_merged_interval[0], max(last_merged_interval[1], current_interval[1])]
        else:
            merged.append(current_interval)
    return merged