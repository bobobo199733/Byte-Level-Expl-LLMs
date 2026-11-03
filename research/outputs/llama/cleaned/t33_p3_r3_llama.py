def heap_sort(values):
    """
    Sorts a list using the heap sort algorithm.

    :param values: The list to be sorted.
    :return: The sorted list.
    """
    build_max_heap(values)
    for i in range(len(values) - 1, 0, -1):
        values[0], values[i] = (values[i], values[0])
        heapify(values, 0, i)
    return values

def build_max_heap(values):
    """
    Builds a max heap from the input list.

    :param values: The list to be converted into a max heap.
    """
    for i in range(len(values) // 2 - 1, -1, -1):
        heapify(values, i, len(values))

def heapify(heap, index, heap_size):
    """
    Maintains the max heap property by moving elements up or down as necessary.

    :param heap: The list to be maintained as a max heap.
    :param index: The current index being processed.
    :param heap_size: The size of the heap (i.e., the number of elements).
    """
    left = 2 * index + 1
    right = 2 * index + 2
    largest = index
    if left < heap_size and heap[left] > heap[largest]:
        largest = left
    if right < heap_size and heap[right] > heap[largest]:
        largest = right
    if largest != index:
        heap[index], heap[largest] = (heap[largest], heap[index])
        heapify(heap, largest, heap_size)