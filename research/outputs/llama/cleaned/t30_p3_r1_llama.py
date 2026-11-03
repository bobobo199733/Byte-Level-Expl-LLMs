def max_subarray_sum(nums):
    """
    This function calculates the maximum sum of a contiguous subarray.

    Args:
        nums (list): A list of integers.

    Returns:
        int: The maximum sum of a contiguous subarray.
    """
    if not nums:
        return 0
    curr_max = overall_max = nums[0]
    for num in nums[1:]:
        curr_max = max(num, curr_max + num)
        overall_max = max(overall_max, curr_max)
    return overall_max