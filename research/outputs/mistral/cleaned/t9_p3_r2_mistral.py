def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for current in intervals:
        last = merged[-1]
        if last[1] >= current[0]:
            last[1] = max(last[1], current[1])
        else:
            merged.append(current)
    return merged