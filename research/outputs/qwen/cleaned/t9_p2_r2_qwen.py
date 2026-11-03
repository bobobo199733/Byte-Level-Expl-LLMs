def merge_intervals(intervals):
    if not intervals:
        return []
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]
    for current_start, current_end in sorted_intervals[1:]:
        last_end = merged[-1][1]
        if current_start <= last_end:
            merged[-1][1] = max(last_end, current_end)
        else:
            merged.append([current_start, current_end])
    return merged