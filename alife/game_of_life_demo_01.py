#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from visualizers import MatrixVisualizer
import numpy as np
import game_of_life_patterns_add

visualizer = MatrixVisualizer()

WIDTH = 50
HEIGHT = 50

state = np.zeros((HEIGHT, WIDTH), dtype=np.int8)
state_gen = np.zeros((HEIGHT, WIDTH), dtype=np.float16)
next_state = np.empty((HEIGHT, WIDTH), dtype=np.int8)
next_state_gen = np.empty((HEIGHT, WIDTH), dtype=np.float16)

pattern = game_of_life_patterns_add.MAX_STATICS_AND_BLINKER

state[0:0 + pattern.shape[0], 0:0 + pattern.shape[1]] = pattern
state_gen[0:0 + pattern.shape[0], 0:0 + pattern.shape[1]] = pattern

while visualizer:

    time.sleep(0.2)  # 秒

    for i in range(HEIGHT):
        for j in range(WIDTH):

            nw = state[i - 1, j - 1]
            n = state[i - 1, j]
            ne = state[i - 1, (j + 1) % WIDTH]
            w = state[i, j - 1]
            c = state[i, j]
            e = state[i, (j + 1) % WIDTH]
            sw = state[(i + 1) % HEIGHT, j - 1]
            s = state[(i + 1) % HEIGHT, j]
            se = state[(i + 1) % HEIGHT, (j + 1) % WIDTH]
            neighbor_cell_sum = nw + n + ne + w + e + sw + s + se
            if c == 0 and neighbor_cell_sum == 3:
                next_state[i, j] = 1
            elif c == 1 and neighbor_cell_sum in (2, 3):
                next_state[i, j] = 1
            else:
                next_state[i, j] = 0
    state, next_state = next_state, state
    visualizer.update(1 - state)
