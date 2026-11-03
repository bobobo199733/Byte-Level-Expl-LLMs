def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[i] < arr[l]:
        largest = l
    if r < n and arr[largest] < arr[r]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = (arr[largest], arr[i])
        heapify(arr, n, largest)

def heap_sort(values):
    n = len(values)
    for i in range(n // 2 - 1, -1, -1):
        heapify(values, n, i)
    sorted_values = values.copy()
    for i in range(n - 1, 0, -1):
        sorted_values[i], sorted_values[0] = (sorted_values[0], sorted_values[i])
        heapify(sorted_values, i, 0)
    return sorted_values