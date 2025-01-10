import heapq
import json
import sys

with open("spb.json", "r", encoding="utf-8") as f:
    stations = json.load(f)

with open("spb_lines.json", "r", encoding="utf-8") as f:
    lines = json.load(f)

with open("spb_transfers.json", "r", encoding="utf-8") as f:
    transfers = json.load(f)


def calc_route(start_station, finish_station):
    if lines[start_station] == lines[finish_station]:  # если станции на одной линии
        no_transfers(start_station, finish_station)
    else:
        with_transfers(stations, start_station, finish_station)


avg_interval = 2


def no_transfers(start_station, finish_station):
    with open("spb_station_nums.json", "r", encoding="utf-8") as f:
        station_nums = json.load(f)

    current_station = start_station
    path = []
    time = avg_interval

    if station_nums[start_station] < station_nums[finish_station]:  # едем с севера на юг
        while current_station != finish_station:
            i = -1
            path.append(current_station)

            next_station = list(stations[current_station].items())[i][0]

            while list(transfers[current_station].items())[i][1]:
                i -= 1
                next_station = list(stations[current_station].items())[i][0]

            time += stations[current_station][next_station]
            current_station = next_station
        path.append(current_station)
        for i in path:
            num_line = lines[i]
            match num_line:
                case 1:
                    print("\033[31m{}".format(i))
                case 2:
                    print("\033[34m{}".format(i))
                case 3:
                    print("\033[32m{}".format(i))
                case 4:
                    print("\033[214m{}".format(i))
                case 5:
                    print("\033[91m{}".format(i))

        print(f"\u001b[0m\nВремя пути (мин):\n {time} мин")

    else:  # едем с юга на север
        while current_station != finish_station:
            path.append(current_station)
            next_station = list(stations[current_station].items())[0][0]

            time += stations[current_station][next_station]
            current_station = next_station
        path.append(current_station)
        for i in path:
            num_line = lines[i]
            match num_line:
                case 1:
                    print("\033[31m{}".format(i))
                case 2:
                    print("\033[34m{}".format(i))
                case 3:
                    print("\033[32m{}".format(i))
                case 4:
                    print("\033[214m{}".format(i))
                case 5:
                    print("\033[91m{}".format(i))

        print(f"\u001b[0m\nВремя пути (мин):\n {time} мин")


def with_transfers(graph, start, end):
    # Инициализация расстояний до всех вершин
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0

    # Инициализация кучи для хранения вершин
    priority_queue = [(0, start)]

    # Словарь для отслеживания путей
    previous_vertices = {vertex: None for vertex in graph}

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # Если достигли конечной вершины, можно завершить
        if current_vertex == end:
            break

        # Пропускаем вершины с большим расстоянием
        if current_distance > distances[current_vertex]:
            continue

        # Обход соседей текущей вершины
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            # Если найден более короткий путь к соседу
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))

    # Восстановление пути от start до end
    path = []
    current_vertex = end
    while current_vertex is not None:
        path.append(current_vertex)
        current_vertex = previous_vertices[current_vertex]

    path.reverse()

    for i in path:
        num_line = lines[i]
        match num_line:
            case 1:
                print("\033[31m{}".format(i))
            case 2:
                print("\033[34m{}".format(i))
            case 3:
                print("\033[32m{}".format(i))
            case 4:
                print("\033[214m{}".format(i))
            case 5:
                print("\033[91m{}".format(i))

    if lines[path[-1]] != lines[path[-2]]:
        distances[end] -= avg_interval

    print(f"\u001b[0m\nВремя пути:\n{str(distances[end] + avg_interval)} мин")


def repeat_program_dialog():
    answer = ""
    while answer != "N" and answer != "Y":
        answer = input("\033[32m{}".format("Хотите попробовать еще? Y/N\n"))
        if answer != "N" and answer != "Y":
            print("\033[31m{}".format("Ошибка! Некорректный ввод!"))
            print("\033[32m{}".format("Вы хотите попробовать еще? Y - да; N - нет\n"))

    if answer == "N":
        print(("\033[32m{}".format("До свидания! Хорошего пути!")))
        sys.exit()
    elif answer == "Y":
        start()


def start():
    while True:
        start_station = input("\033[37m{}".format("Введите начальную станцию вашего маршрута:\n"))
        finish_station = input("\033[37m{}".format("Введите конечную станцию вашего маршрута:\n"))
        try:
            calc_route(start_station, finish_station)
            if start_station == finish_station:
                print("\033[31m{}".format("Ошибка! Начало и конец маршрута совпадают!"))
                repeat_program_dialog()
            repeat_program_dialog()

        except KeyError:
            print("\033[31m{}".format("Ошибка! Неверно введено название станции!\n"
                                      "Возможно вы допустили опечатку, "
                                      "написали название станции не кириллицей или не с заглавной буквы"))
            repeat_program_dialog()


if __name__ == '__main__':
    start()
