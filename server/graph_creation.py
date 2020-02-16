import numpy as np
import matplotlib.pyplot as plt
import sqlite3


def create_status_day_graph(stats_list):
    stats_num = len(stats_list)

    ind_stats_nums = [0, 0, 0, 0]
    for stat in stats_list:
        if stat == 'offline':
            ind_stats_nums[0] += 1
        elif stat == 'online':
            ind_stats_nums[1] += 1
        elif stat == 'idle':
            ind_stats_nums[2] += 1
        elif stat == 'dnd':
            ind_stats_nums[3] += 1

    labels = []
    labels_names = 'Offline', 'Online', 'Idle', 'Do Not Disturb'
    sizes = []
    for i in range(len(ind_stats_nums)):
        if ind_stats_nums[i] > 0:
            labels.append(labels_names[i])
            sizes.append(int(ind_stats_nums[i] / stats_num * 100))

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=0)
    ax1.axis('equal')
    plt.savefig('status_day_graph.png')


def create_status_week_graph(stats_list):
    N = 5
    menMeans = (20, 35, 30, 35, 27)
    womenMeans = (25, 32, 34, 20, 25)

    online = []
    offline = []
    idle = []
    dnd = []
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35  # the width of the bars: can also be len(x) sequence

    p1 = plt.bar(ind, menMeans, width)
    p2 = plt.bar(ind, womenMeans, width,
                 bottom=menMeans)

    plt.ylabel('Percentages')
    plt.title('Statuses by Day and Percentage of Day')
    plt.xticks(ind, ('Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5'))
    plt.yticks(np.arange(0, 101, 10))
    plt.legend((p1[0], p2[0]), ('Online', 'Offline'))

    plt.show()
