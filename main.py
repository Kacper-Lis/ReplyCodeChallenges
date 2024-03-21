def parse_data(file_name):
    pass


def output_results(file_name):
     with open(f'out_{file_name}.txt', mode='w') as file:
        for row in data_solution:
            file.write(row + '\n')
        pass


def solution():
    results = ["solution1", "solution2"]
    return results


if __name__ == "__main__":
    file_0 = ""
    file_1 = ""
    file_2 = ""
    file_3 = ""
    file_4 = ""
    file_5 = ""
    file_6 = ""

    current_file = file_1

    data = parse_data(current_file)

    data_solution = solution()

    output_results(current_file)
