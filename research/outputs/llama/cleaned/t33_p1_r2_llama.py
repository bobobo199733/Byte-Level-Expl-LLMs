def heap_sort(values):
    """
    Sorts a list of values using the Heap Sort algorithm.

    Args:
        values (list): The list to be sorted.

    Returns:
        list: A new sorted list.
    """
    build_max_heap(values)
    sorted_values = []
    while len(values) > 0:
        max_value = heap_extract_max(values)
        sorted_values.append(max_value)
    return sorted_values

def build_max_heap(values):
    """
    Builds a max-heap from the given values.

    Args:
        values (list): The list of values.
    """
    for i in range(len(values) // 2 - 1, -1, -1):
        heapify(values, len(values), i)

def heapify(heap, n, i):
    """
    Heapifies the subtree rooted at index i.

    Args:
        heap (list): The list to be heapified.
        n (int): The size of the heap.
        i (int): The root of the subtree to be heapified.
    """
    largest = i
    left_child_index = 2 * i + 1
    if left_child_index < n and heap[left_child_index] > heap[largest]:
        largest = left_child_index
    right_child_index = 2 * i + 2
    if right_child_index < n and heap[right_child_index] > heap[largest]:
        largest = right_child_index
    if largest != i:
        heap[i], heap[largest] = (heap[largest], heap[i])
        heapify(heap, n, largest)

def heap_extract_max(heap):
    """
    Removes and returns the maximum element from the heap.

    Args:
        heap (list): The list to be modified.

    Returns:
        int: The maximum value.
    """
    max_value = heap[0]
    heap[0] = heap[-1]
    heap.pop()
    heapify(heap, len(heap), 0)
    return max_value