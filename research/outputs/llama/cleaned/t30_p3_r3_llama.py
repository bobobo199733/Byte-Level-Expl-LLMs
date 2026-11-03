def max_subarray_sum(nums):
    """
    This function calculates the maximum sum of a contiguous subarray within a given list of numbers.

    Args:
        nums (list): A list of integers.

    Returns:
        int: The maximum sum of a contiguous subarray.
    """
    max_current = max_global = nums[0]
    for num in nums[1:]:
        max_current = max(num, max_current + num)
        max_global = max(max_global, max_current)
    return max_global