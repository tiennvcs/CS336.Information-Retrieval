def partition(array, start, end):
    
    pivot = array[start]
    low = start + 1
    high = end

    while True:
        while low <= high and array[high] >= pivot:
            high = high - 1

        # Opposite process of the one above
        while low <= high and array[low] <= pivot:
            low = low + 1

        # We either found a value for both high and low that is out of order
        # or low is higher than high, in which case we exit the loop
        if low <= high:
            array[low], array[high] = array[high], array[low]
            # The loop continues
        else:
            # We exit out of the loop
            break

    array[start], array[high] = array[high], array[start]

    return high


def quicksort(arr, start, end):
    if start >= end:
        return
    p = partition(arr, start, end)
    quick_sort(arr, start, p-1)
    quick_sort(arr, p+1, end)


def merge_sort(arr):
    return None