import time
from algorithms.Settings import get_global_delay

comparisons = 0
swaps = 0

def quicksort_recursive (arr, low, high, canvas, element_ids, algorithm_information):
    if low < high:
        pivotIndex = partition(arr, low, high, canvas, element_ids, algorithm_information)

        quicksort_recursive(arr, low, pivotIndex - 1, canvas, element_ids, algorithm_information)
        quicksort_recursive(arr, pivotIndex + 1, high, canvas, element_ids, algorithm_information)
    return arr


def partition (arr, low, high, canvas, element_ids, algorithm_information):
    global comparisons, swaps
    pivot = arr[high]
    if get_global_delay() != 0:
        canvas.itemconfig(element_ids[high], fill="green")
        canvas.update()
        time.sleep(get_global_delay())
    i = low - 1

    for j in range(low, high):
        comparisons += 1
        algorithm_information.set("comparisons: " + str(comparisons) + "       swaps: " + str(swaps) + "     ")
        if get_global_delay() != 0:
            canvas.itemconfig(element_ids[j], fill="red")
            canvas.update()
            time.sleep(get_global_delay())
        if arr[j] < pivot:
            i += 1
            if i != j:
                swap(arr, i, j, canvas, element_ids, algorithm_information)
        canvas.itemconfig(element_ids[j], fill="black")
    if i + 1 != high:
        swap(arr, i + 1, high, canvas, element_ids, algorithm_information)
    canvas.itemconfig(element_ids[i+1], fill="black")
    return i + 1

def swap(data, index_a, index_b, canvas, element_ids, algorithm_information):
    global comparisons, swaps
    swaps += 1
    algorithm_information.set("comparisons: " + str(comparisons) + "       swaps: " + str(swaps) + "     ")
    tempValue = data[index_a]
    data[index_a] = data[index_b]
    data[index_b] = tempValue

    if get_global_delay() != 0:
        canvas.itemconfig(element_ids[index_a], fill="cyan")
        canvas.itemconfig(element_ids[index_b], fill="cyan")
        canvas.update()
        time.sleep(get_global_delay())

    coords_a = canvas.coords(element_ids[index_a])
    coords_b = canvas.coords(element_ids[index_b])

    # Calculate the difference in x-coordinates between the two elements
    dx = coords_a[0] - coords_b[0]

    # Move the elements to their new positions
    canvas.move(element_ids[index_a], -dx, 0)
    canvas.move(element_ids[index_b], dx, 0)

    # switch the elements ids
    element_ids[index_a], element_ids[index_b] = element_ids[index_b], element_ids[index_a]

    if get_global_delay() != 0:
        canvas.itemconfig(element_ids[index_a], fill="black")
        canvas.itemconfig(element_ids[index_b], fill="black")
        canvas.update()