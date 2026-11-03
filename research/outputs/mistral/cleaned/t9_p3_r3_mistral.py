def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for interval in intervals:
        last_merged = merged[-1]
        if last_merged[1] < interval[0]:
            merged.append(interval)
        else:
            last_merged[1] = max(last_merged[1], interval[1])
    return merged