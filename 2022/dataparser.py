import data
from data import Demon


def parse_data(file_name):
    demons_array = []
    first_line = None
    with open(file_name) as file:
        for line in file:
            if first_line:
                arr = line.split()
                demons_array.append(Demon(int(arr[0]), int(arr[1]), int(arr[2]), int(arr[3]), arr[4:]))
                data.serial_ID += 1
            else:
                first_line = line.split()
    return first_line, demons_array
