def heap_sort(values):
    """
    Heap sort algorithm implementation.

    :param values: List of elements to be sorted
    :return: Sorted list
    """

    def build_max_heap(arr, n):
        for i in range(n // 2 - 1, -1, -1):
            heapify(arr, n, i)

    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = (arr[largest], arr[i])
            heapify(arr, n, largest)

    def extract_max_heap(arr):
        n = len(arr)
        root = arr[0]
        arr[0] = arr[n - 1]
        n -= 1
        heapify(arr, n, 0)
        return root
    build_max_heap(values, len(values))
    for i in range(len(values) - 1, 0, -1):
        max_element = extract_max_heap(values)
        values[i] = max_element
    return values