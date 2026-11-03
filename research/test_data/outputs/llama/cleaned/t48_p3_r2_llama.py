def median_of_two_sorted_arrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = (nums2, nums1)
    x, y = (len(nums1), len(nums2))
    start = 0
    end = x
    while start <= end:
        partitionX = (start + end) // 2
        partitionY = (x + y + 1) // 2 - partitionX
        maxLeftX = float('-inf') if partitionX == 0 else nums1[partitionX - 1]
        minRightX = float('inf') if partitionX == x else nums1[partitionX]
        maxLeftY = float('-inf') if partitionY == 0 else nums2[partitionY - 1]
        minRightY = float('inf') if partitionY == y else nums2[partitionY]
        if maxLeftX <= minRightY and maxLeftY <= minRightX:
            if (x + y) % 2 == 1:
                return max(maxLeftX, maxLeftY)
            else:
                return (max(maxLeftX, maxLeftY) + min(minRightX, minRightY)) / 2
        elif maxLeftX > minRightY:
            end = partitionX - 1
        else:
            start = partitionX + 1