#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import game_of_life_patterns
from quantum_game_of_life import quantum_2d_cellular_automaton

# pattern = game_of_life_patterns.CENTER_20
CENTER_20 = np.array(
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
     [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])


def plot_graph(x, y, graph_file):
    x = df['time_step']
    y = df['data']
    f2 = interp1d(x, y, kind='cubic')
    new = np.linspace(1, len(y), endpoint=True)
    fig = plt.figure()
    plt.plot(x, y, 'o', new, f2(new), '-')
    plt.legend(['data', 'cubic'], loc='best')
    fig.savefig(graph_file)
    # plt.show()


# 出力フォルダ
path = 'D:/github/quantum_alife/alife/'

# data_20220610_170757
timestamp = "{0:%Y%m%d_%H%M%S}".format(datetime.datetime.now())
data_file = path + 'data_' + timestamp + '.txt'
graph_file = path + 'data_graph_' + timestamp + '.png'
df = quantum_2d_cellular_automaton(width=20, height=20, pattern=CENTER_20,
                                   env_interaction_theta=math.pi / 8, death_value=0.2,
                                   non_live=[0, 1], live_theta=math.pi / 4, live_low=0.1, live_high=0.5,
                                   data_file=True, data_file_name=data_file, data_num=10, shots=100)
plot_graph(df['time_step'], df['data'], graph_file)

