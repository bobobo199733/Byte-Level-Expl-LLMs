def heap_sort(values):
    """
    Sorts a list of integers in ascending order using the heap sort algorithm.

    Args:
        values (list): The input list to be sorted.

    Returns:
        list: A new sorted list.
    """
    sorted_values = values[:]
    build_max_heap(sorted_values)
    while len(sorted_values) > 1:
        max_element = sorted_values[0]
        sorted_values[0] = sorted_values[-1]
        sorted_values.pop()
        restore_max_heap(sorted_values, 0)
    return sorted_values

def build_max_heap(heap):
    """
    Builds a max-heap from the given list.

    Args:
        heap (list): The input list to be heapified.
    """
    for i in range(len(heap) // 2 - 1, -1, -1):
        restore_max_heap(heap, i)

def restore_max_heap(heap, index):
    """
    Restores the max-heap property at the given index.

    Args:
        heap (list): The input list to be heapified.
        index (int): The current node index.
    """
    left_child = 2 * index + 1
    right_child = 2 * index + 2
    max_element_index = index
    if left_child < len(heap) and heap[left_child] > heap[max_element_index]:
        max_element_index = left_child
    if right_child < len(heap) and heap[right_child] > heap[max_element_index]:
        max_element_index = right_child
    if max_element_index != index:
        heap[index], heap[max_element_index] = (heap[max_element_index], heap[index])
        restore_max_heap(heap, max_element_index)