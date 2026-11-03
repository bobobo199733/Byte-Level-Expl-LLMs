def kth_largest(nums, k):

    def quickselect(arr, low, high, k):
        if low < high:
            j = partition(arr, low, high)
            if j == k:
                return arr[j]
            elif j > k:
                return quickselect(arr, low, j - 1, k)
            else:
                return quickselect(arr, j + 1, high, k)

    def partition(arr, low, high):
        pivot = arr[high]
        i = low
        for j in range(low, high):
            if arr[j] >= pivot:
                arr[i], arr[j] = (arr[j], arr[i])
                i += 1
        arr[i], arr[high] = (arr[high], arr[i])
        return i
    return quickselect(nums, 0, len(nums) - 1, len(nums) - k)