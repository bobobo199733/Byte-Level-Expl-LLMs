def merge_intervals(intervals):
    if not intervals:
        return []
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged_intervals = [sorted_intervals[0]]
    for interval in sorted_intervals[1:]:
        last_merged = merged_intervals[-1]
        if interval[0] <= last_merged[1]:
            last_merged[1] = max(last_merged[1], interval[1])
        else:
            merged_intervals.append(interval)
    return merged_intervals