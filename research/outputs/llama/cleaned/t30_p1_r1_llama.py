def max_subarray_sum(nums):
    """
    Returns the maximum sum of any contiguous subarray.

    Args:
        nums (list): A list of integers.

    Returns:
        int: The maximum sum of a subarray.

    Raises:
        ValueError: If the input list is empty.
    """
    if not nums:
        raise ValueError('Input list cannot be empty')
    max_sum = float('-inf')
    current_sum = 0
    for num in nums:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum