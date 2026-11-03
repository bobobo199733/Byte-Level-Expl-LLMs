def heapify(arr, n, i):
    largest = i
    left_child = 2 * i + 1
    right_child = 2 * i + 2
    if left_child < n and arr[i] < arr[left_child]:
        largest = left_child
    if right_child < n and arr[largest] < arr[right_child]:
        largest = right_child
    if largest != i:
        arr[i], arr[largest] = (arr[largest], arr[i])
        heapify(arr, n, largest)

def heap_sort(values):
    n = len(values)
    for i in range(n // 2 - 1, -1, -1):
        heapify(values, n, i)
    sorted_list = []
    for i in range(n - 1, 0, -1):
        values[0], values[i] = (values[i], values[0])
        sorted_list.append(values.pop())
        heapify(values, i, 0)
    return sorted_list[::-1]