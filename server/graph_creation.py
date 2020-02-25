import numpy as np
import matplotlib.pyplot as plt
import sqlite3


def create_status_pie_graph(stats_list):
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

    colors_list = []
    if 'Offline' in labels:
        colors_list.append('grey')
    if 'Online' in labels:
        colors_list.append('green')
    if 'Idle' in labels:
        colors_list.append('orange')
    if 'Do Not Disturb' in labels:
        colors_list.append('red')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=0, colors=colors_list)
    ax1.axis('equal')
    plt.savefig('status_pie_graph.png')


def create_status_bar_graph(stats_list):
    num_of_days = len(stats_list)

    online = []
    offline = []
    idle = []
    dnd = []

    for day in stats_list:
        day_stats_nums = [0, 0, 0, 0]
        for stat in day:
            if stat == 'offline':
                day_stats_nums[1] += 1
            elif stat == 'online':
                day_stats_nums[0] += 1
            elif stat == 'idle':
                day_stats_nums[2] += 1
            elif stat == 'dnd':
                day_stats_nums[3] += 1

        if len(day) != 0:
            online.append(int(day_stats_nums[0] / len(day) * 100))
            offline.append(int(day_stats_nums[1] / len(day) * 100))
            idle.append(int(day_stats_nums[2] / len(day) * 100))
            dnd.append(int(day_stats_nums[3] / len(day) * 100))
        else:
            online.append(0)
            offline.append(0)
            idle.append(0)
            dnd.append(0)

    print(online)
    print(offline)
    print(idle)
    print(dnd)

    ind = np.arange(num_of_days)  # the x locations for the groups
    width = 0.35  # the width of the bars: can also be len(x) sequence

    p1 = plt.bar(ind, online, width, color='green')
    p2 = plt.bar(ind, offline, width, bottom=online, color='grey')
    p3 = plt.bar(ind, idle, width, bottom=np.array(offline)+np.array(online), color='orange')
    p4 = plt.bar(ind, dnd, width, bottom=np.array(idle)+np.array(offline)+np.array(online), color='red')

    plt.ylabel('Percent')
    plt.title('Statuses by Day and Percentage of Day')
    plt.xlabel('Days Ago')
    names_list = []
    for day in range(num_of_days):
        names_list.append(str(day))
    plt.xticks(ind, names_list)
    plt.yticks(np.arange(0, 101, 10))
    plt.legend((p1[0], p2[0], p3[0], p4[0]), ('Online', 'Offline', 'Idle', 'Do Not Disturb'))

    plt.savefig('status_bar_graph.png')
