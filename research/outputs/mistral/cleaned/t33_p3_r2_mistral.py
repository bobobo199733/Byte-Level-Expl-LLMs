def build_heap(values):
    n = len(values)
    for i in range(n // 2 - 1, -1, -1):
        heapify_helper(i, n, values)

def heapify_helper(i, n, values):
    left = 2 * i + 1
    right = 2 * i + 2
    largest = i
    if left < n and values[left] > values[largest]:
        largest = left
    if right < n and values[right] > values[largest]:
        largest = right
    if largest != i:
        values[i], values[largest] = (values[largest], values[i])
        heapify_helper(largest, n, values)

def heap_sort(values):
    build_heap(values)
    for i in range(len(values) - 1, 0, -1):
        values[0], values[i] = (values[i], values[0])
        heapify_helper(0, i, values)