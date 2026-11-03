def max_subarray_sum(nums):
    """
    This function calculates the maximum sum of a contiguous subarray.

    Args:
        nums (list): A list of integers representing the array.

    Returns:
        int: The maximum sum of a contiguous subarray.
    """
    current_max = overall_max = nums[0]
    for num in nums[1:]:
        current_max = max(num, current_max + num)
        overall_max = max(overall_max, current_max)
    return overall_max