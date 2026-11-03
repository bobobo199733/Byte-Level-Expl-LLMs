def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for interval in intervals:
        last_interval = merged[-1]
        if interval[0] > last_interval[1]:
            merged.append(interval)
        else:
            last_interval[1] = max(last_interval[1], interval[1])
    return merged