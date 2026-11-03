def max_subarray_sum(nums):
    """
    Find the maximum sum of any contiguous subarray within a given one-dimensional array.

    Parameters:
    nums (List[int]): A list of integers.

    Returns:
    int: The maximum subarray sum.
    """
    if not nums:
        return 0
    current_sum = max_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum