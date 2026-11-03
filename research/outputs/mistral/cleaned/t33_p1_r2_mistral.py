def create_heap(arr, n, i=None):
    if i is None:
        i = n // 2 - 1
    while i >= 0:
        heapify(arr, n, i)
        i -= 1

def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = (arr[largest], arr[i])
        heapify(arr, n, largest)

def heap_sort(values):
    n = len(values)
    create_heap(values, n)
    for i in range(n - 1, 0, -1):
        values[0], values[-i] = (values[-i], values[0])
        create_heap(values, i)
    return values