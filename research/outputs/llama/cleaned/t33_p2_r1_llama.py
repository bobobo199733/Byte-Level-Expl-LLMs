def heap_sort(values):
    """
    Sorts a list of integers in ascending order using the Heap Sort algorithm.

    :param values: A list of integers to be sorted.
    :return: A new sorted list containing the same integers as the input.
    """
    if not values:
        return []
    heap = values[:]
    build_max_heap(heap)
    for end_idx in range(len(heap) - 1, 0, -1):
        heap[0], heap[end_idx] = (heap[end_idx], heap[0])
        re_heapify(heap, 0, end_idx)
    return heap

def build_max_heap(arr):
    """
    Builds a max heap structure within an input array.

    :param arr: A list of integers that will be transformed into a max heap.
    """
    for i in range(len(arr) // 2 - 1, -1, -1):
        re_heapify(arr, i, len(arr))

def re_heapify(heap, idx, end_idx):
    """
    Re-establishes the max heap property at a given index within an array.

    :param heap: A list of integers representing a max heap structure.
    :param idx: The index of the element to be re-heapified.
    :param end_idx: The current right boundary of the sub-tree rooted at idx.
    """
    largest = 2 * idx + 1
    while largest < end_idx:
        if largest + 1 < end_idx and heap[largest + 1] > heap[largest]:
            largest += 1
        if heap[largest] > heap[idx]:
            heap[largest], heap[idx] = (heap[idx], heap[largest])
            idx = largest
            largest = 2 * idx + 1
        else:
            break