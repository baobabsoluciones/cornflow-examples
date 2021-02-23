'''
This file contains the input data for the problem
'''
stations = ['station1', 'station2', 'station3', 'station4']

no_position_station = {'station1': 1.0, 'station2': 1.0, 'station3': 1.0, 'station4': 1.0}

tasks = ['task1', 'task2', 'task3', 'task4', 'task5', 'task6', 'task7', 'task8', 'task9', 'task10', 'task11', 'task12']

tasks_duration = {'task1': 3.0, 'task2': 6.0, 'task3': 7.0, 'task4': 6.0, 'task5': 5.0, 'task6': 8.0, 'task7': 9.0,
                  'task8': 11.0, 'task9': 2.0, 'task10': 13.0, 'task11': 4.0, 'task12': 3.0}
precedences = {'task1': ['task2', 'task3'],
               'task2': ['task4', 'task5', 'task6'],
               'task3': ['task6', 'task7'],
               'task6': ['task8'],
               'task4': ['task9'],
               'task5': ['task9'],
               'task8': ['task9', 'task10'],
               'task11': ['task10'],
               'task7': ['task11'],
               'task9': ['task12'],
               'task10': ['task12']}


station_order = {'station1': 1.0, 'station2': 2.0, 'station3': 3.0, 'station4': 4.0}

data = dict(stations=stations,
            no_position_station=no_position_station,
            tasks=tasks,
            tasks_duration=tasks_duration,
            precedences=precedences,
            station_order=station_order)
