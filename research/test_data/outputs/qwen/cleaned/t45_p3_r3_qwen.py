def search_insert_position(nums, target):
    """
    Finds the index or insertion position in a sorted array where the target should be placed.
    
    :param nums: List[int] - A list of integers that is already sorted in ascending order.
    :param target: int - The target integer to find the insertion position for.
    :return: int - The index at which the target should be inserted.
    """
    left, right = (0, len(nums) - 1)
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return left