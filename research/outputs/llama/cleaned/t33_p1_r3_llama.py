def heap_sort(values):
    """
    Sorts a list using the heap sort algorithm.

    Args:
        values (list): The list to be sorted.

    Returns:
        list: A new sorted list.
    """
    sorted_values = values[:]

    def build_max_heap(values):
        for i in range(len(values) // 2 - 1, -1, -1):
            heapify(values, i)

    def heapify(values, i):
        left_child = 2 * i + 1
        right_child = 2 * i + 2
        largest = i
        if left_child < len(values) and values[left_child] > values[largest]:
            largest = left_child
        if right_child < len(values) and values[right_child] > values[largest]:
            largest = right_child
        if largest != i:
            values[i], values[largest] = (values[largest], values[i])
            heapify(values, largest)
    build_max_heap(sorted_values)
    for i in range(len(sorted_values) - 1, 0, -1):
        sorted_values[0], sorted_values[i] = (sorted_values[i], sorted_values[0])
        heapify(sorted_values, 0)
        sorted_values.pop()
    return sorted_values