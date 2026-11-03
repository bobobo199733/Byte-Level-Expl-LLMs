def create_heap(arr, n, i=None):
    if i is None:
        i = len(arr) // 2 - 1
    for j in range(i, -1, -1):
        max_index = j
        left_child = 2 * j + 1
        right_child = 2 * j + 2
        if left_child < n and arr[left_child] > arr[max_index]:
            max_index = left_child
        if right_child < n and arr[right_child] > arr[max_index]:
            max_index = right_child
        if j != max_index:
            arr[j], arr[max_index] = (arr[max_index], arr[j])
            create_heap(arr, n, max_index)

def heap_sort(values):
    n = len(values)
    for i in range(n // 2 - 1, -1, -1):
        create_heap(values, n, i)
    for i in range(n - 1, 0, -1):
        values[i], values[0] = (values[0], values[i])
        create_heap(values, i)
    return values