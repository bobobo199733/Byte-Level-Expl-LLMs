def heap_sort(values):
    """
    Sorts a list using the Heap Sort algorithm.

    Args:
        values (list): The list to sort.

    Returns:
        list: A new sorted list.
    """

    def build_max_heap(arr):
        n = len(arr)
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
        sorted_list = []
        while n > 0:
            sorted_list.append(arr[0])
            arr[0] = arr[n - 1]
            n -= 1
            heapify(arr, n, 0)
        return sorted_list
    values_copy = values[:]
    build_max_heap(values_copy)
    sorted_list = extract_max_heap(values_copy)
    return sorted_list