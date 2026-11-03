def autocomplete_system(words, prefix):
    if not words or not prefix:
        return []

    def bin_search(arr, target):
        low = 0
        high = len(arr) - 1
        while low <= high:
            mid = (low + high) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] > target:
                high = mid - 1
            else:
                low = mid + 1
        return None
    results = []
    for word in words:
        if word.startswith(prefix) and bin_search(results, word) is None:
            results.append(word)
    results.sort()
    return results