def heap_sort(values):
    """
    Sorts a list in ascending order using the Heap Sort algorithm.

    :param values: List to be sorted
    :return: Sorted list
    """

    def _build_max_heap(arr, n):
        for i in range(n // 2 - 1, -1, -1):
            _heapify(arr, n, i)

    def _heapify(arr, n, i):
        largest = i
        left_child = 2 * i + 1
        right_child = 2 * i + 2
        if left_child < n and arr[left_child] > arr[largest]:
            largest = left_child
        if right_child < n and arr[right_child] > arr[largest]:
            largest = right_child
        if largest != i:
            arr[i], arr[largest] = (arr[largest], arr[i])
            _heapify(arr, n, largest)

    def _sift_down(arr):
        for i in range(len(arr) - 1, 0, -1):
            if arr[0] < arr[i]:
                arr[0], arr[i] = (arr[i], arr[0])
                _heapify(arr, i, 0)
    n = len(values)
    _build_max_heap(values, n)
    for i in range(n - 1, 0, -1):
        _sift_down(values[:i + 1])
    return values