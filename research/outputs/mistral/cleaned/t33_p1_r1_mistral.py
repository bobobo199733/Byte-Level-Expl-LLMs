def create_heap(values):
    n = len(values)
    for i in range(n // 2 - 1, -1, -1):
        heapify_helper(values, n, i)

def heapify_helper(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = (arr[largest], arr[i])
        heapify_helper(arr, n, largest)

def heap_sort(values):
    create_heap(values)
    for i in range(len(values) - 1, 0, -1):
        values[0], values[i] = (values[i], values[0])
        heapify_helper(values, i, 0)
    return values