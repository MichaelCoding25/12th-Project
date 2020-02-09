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
    plt.show()
