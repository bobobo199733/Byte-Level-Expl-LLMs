def kth_largest(nums, k):

    def quickselect(arr, low, high, k):
        if low < high:
            pivot = partition(arr, low, high)
            if pivot == k:
                return arr[pivot]
            elif pivot > k:
                return quickselect(arr, low, pivot - 1, k)
            else:
                return quickselect(arr, pivot + 1, high, k)

    def partition(arr, low, high):
        pivot = arr[high]
        i = low
        for j in range(low, high):
            if arr[j] > pivot:
                arr[i], arr[j] = (arr[j], arr[i])
                i += 1
        arr[i], arr[high] = (arr[high], arr[i])
        return i
    return quickselect(nums, 0, len(nums) - 1, len(nums) - k)