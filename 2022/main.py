import dataparser


class Object:
    def __init__(self, some_num):
        self.some_num = some_num

    def __str__(self):
        return self.some_num

    def __repr__(self):
        return f'{self.some_num}'


def test_sort(arr):
    return arr.sort(key=lambda x: x.some_num)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_0 = '00-example.txt'
    file_1 = '01-the-cloud-abyss.txt'
    file_2 = '02-iot-island-of-terror.txt'
    file_3 = '03-etheryum.txt'
    file_4 = '04-the-desert-of-autonomous-machines.txt'
    file_5 = '05-androids-armageddon.txt'
    current_file = file_5
    first_line, demons_array = dataparser.parse_data(current_file)
    start_stamina = int(first_line[0])
    max_stamina = int(first_line[1])
    turns = int(first_line[2])
    demons = int(first_line[3])
    stamina = start_stamina
    fights = []
    demons_fought = []
    demons_array.sort(key=lambda x: x.max_point, reverse=True)
    for turn in range(turns):
        demon_to_fight = None
        turns_left = turns - turn
        # Stamina management and points calculate
        for demon in demons_fought:
            recover = demon.tick(turn)
            # print(recover)
            stamina += recover
        # Find demon to fight
        for demon in demons_array:
            if stamina - demon.S < 0 or demon.calcualte_points(turns_left) <= 0:
                continue
            demon_to_fight = demon
            break

        # Fight
        if demon_to_fight is not None:
            demon_to_fight.fight(turn)
            demons_fought.append(demon_to_fight)
            fights.append(demon_to_fight.ID)
            stamina -= demon_to_fight.S
            demons_array.remove(demon_to_fight)

    print(fights)
    with open(f'out_{current_file}.txt', mode='w') as file:
        for i in fights:
            file.write(str(i) + '\n')






