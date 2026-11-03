def merge_intervals(intervals):
    if not intervals or len(intervals) == 0:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for i in range(1, len(intervals)):
        last_interval = merged[-1]
        current_interval = intervals[i]
        if last_interval[1] >= current_interval[0]:
            last_interval[1] = max(last_interval[1], current_interval[1])
        else:
            merged.append(current_interval)
    return merged