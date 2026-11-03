def heap_sort(values):
    """
    Sorts a list of integers using the heap sort algorithm.

    Args:
        values (list): A list of integers to be sorted.

    Returns:
        list: A new list containing the same elements as the input, but in sorted order.
    """
    if not values:
        return []

    def build_max_heap(values):
        for i in range(len(values) // 2 - 1, -1, -1):
            _heapify(values, len(values), i)

    def _heapify(values, heap_size, index):
        left_child = 2 * index + 1
        right_child = 2 * index + 2
        largest = index
        if left_child < heap_size and values[left_child] > values[largest]:
            largest = left_child
        if right_child < heap_size and values[right_child] > values[largest]:
            largest = right_child
        if largest != index:
            values[index], values[largest] = (values[largest], values[index])
            _heapify(values, heap_size, largest)
    build_max_heap(values)
    sorted_values = []
    while len(values) > 1:
        sorted_values.append(values[0])
        values[0] = values[-1]
        values.pop()
        _heapify(values, len(values), 0)
    sorted_values.append(values[0])
    return sorted_values