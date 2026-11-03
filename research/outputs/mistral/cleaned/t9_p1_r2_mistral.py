def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged_intervals = [intervals[0]]
    for interval in intervals:
        last_merged = merged_intervals[-1]
        if interval[0] > last_merged[1]:
            merged_intervals.append(interval)
        else:
            last_merged[1] = max(last_merged[1], interval[1])
    return merged_intervals