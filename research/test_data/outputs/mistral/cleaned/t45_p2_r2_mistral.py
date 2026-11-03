def search_insert_position(nums, target):

    def check_valid_input(lst, val):
        if not isinstance(lst, list) or not all((isinstance(i, (int, float)) for i in lst)):
            raise ValueError('Invalid input: nums must be a sorted list of numbers')
        if not isinstance(val, (int, float)):
            raise ValueError('Invalid input: target must be a number')
    check_valid_input(nums, target)
    left = 0
    right = len(nums)
    mid = 0
    while left < right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    if nums and nums[-1] < target:
        return len(nums)
    elif not nums or nums[0] > target:
        return 0
    else:
        return binary_search_insert_index(nums, target, 0, len(nums))

def binary_search_insert_index(arr, val, low, high):
    if low < high:
        mid = (low + high) // 2
        if arr[mid] == val:
            return mid
        elif arr[mid] < val:
            return binary_search_insert_index(arr, val, mid + 1, high)
        else:
            return binary_search_insert_index(arr, val, low, mid - 1)
    elif arr[-1] < val:
        return len(arr)
    elif arr[0] > val:
        return 0
    else:
        return 0