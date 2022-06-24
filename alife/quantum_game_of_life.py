#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np
import pandas as pd
from visualizers import MatrixVisualizer
from qiskit import QuantumCircuit, execute, Aer


def quantum_2d_cellular_automaton(width=20,
                                  height=20,
                                  pattern=[[1, 1], [1, 1]],
                                  env_interaction_theta=math.pi / 8,
                                  death_value=0.2,
                                  non_live=[0, 1],
                                  live_theta=math.pi / 4,
                                  live_low=0.1,
                                  live_high=0.5,
                                  data_file=False,
                                  data_file_name='',
                                  data_num=100,
                                  shots=1000):
    """
    量子二次元セルラー・オートマトンを描画する。

    Parameters
    ----------
    width : int
        描画パラメータ。描画領域の横グリッド数。
    height : int
        描画パラメータ。描画領域の縦グリッド数。
    pattern : list of int
        開始時の初期パターン。
    env_interaction_theta : float
        寿命パラメータ。環境相互作用の強さ、0～pi/2（0で影響なし、pi/2で最大（一度でゼロになる））、TODO：ランダムに決定
    death_value : float
        寿命パラメータ。生き残り条件の閾値（寿命[0～1]がこの値を下回ると死）
    non_live : list of int
        生存パラメータ。出生されない条件。
    live_theta : float
        生存パラメータ。出生時の作用の強さ。
    live_low : float
        生存パラメータ。創発時の下限閾値（値が大きいと生まれにくい、疎状態の評価）。
    live_high : float
        生存パラメータ。創発時の上限閾値（値が小さいと生まれにくい、密状態の評価 ）
    data_file : bool
        ファイルパラメータ。ファイル出力する場合はTrue。
    data_file_name : str
        ファイルパラメータ。ファイルのフルパス（ファイル名含む）。
    data_num : int
        ファイルパラメータ。
    shots : int
        量子回路パラメータ。量子回路の実行回数（ショット数）。
    """

    # visualizerの初期化
    visualizer = MatrixVisualizer()

    # 初期化
    # 初期状態（01の配列）
    state = np.zeros((height, width), dtype=np.int8)
    state[0:0 + pattern.shape[0], 0:0 + pattern.shape[1]] = pattern
    next_state = np.empty((height, width), dtype=np.int8)
    # 遺伝子型の初期化（01の配列、以降は0～1の連続値）
    state_gen = np.zeros((height, width), dtype=np.float16)
    state_gen[0:0 + pattern.shape[0], 0:0 + pattern.shape[1]] = pattern
    next_state_gen = np.empty((height, width), dtype=np.float16)

    # radian値への変換（1～0 → -1～1）
    def encode(x):
        return math.acos(-x * 2 + 1)

    # 期待値の計算
    def getExpectedValue(count):
        return [count[a] / shots if a in count else 0 for a in ['0', '1']]

    loop = 0  # ループ数
    out = []  # 出力データ

    while visualizer:

        loop += 1
        print('loop=', loop)
        count_tmp = 0

        for i in range(height):
            for j in range(width):
                # 自分と近傍のセルの状態を取得
                # c: center (自分自身)
                # nw: north west, ne: north east, c: center ...
                nw = state[i - 1, j - 1]
                n = state[i - 1, j]
                ne = state[i - 1, (j + 1) % width]
                w = state[i, j - 1]
                c = state[i, j]
                e = state[i, (j + 1) % width]
                sw = state[(i + 1) % height, j - 1]
                s = state[(i + 1) % height, j]
                se = state[(i + 1) % height, (j + 1) % width]

                neighbor_cell_sum = nw + n + ne + w + e + sw + s + se

                nw_gen = state_gen[i - 1, j - 1]
                n_gen = state_gen[i - 1, j]
                ne_gen = state_gen[i - 1, (j + 1) % width]
                w_gen = state_gen[i, j - 1]
                c_gen = state_gen[i, j]
                e_gen = state_gen[i, (j + 1) % width]
                sw_gen = state_gen[(i + 1) % height, j - 1]
                s_gen = state_gen[(i + 1) % height, j]
                se_gen = state_gen[(i + 1) % height, (j + 1) % width]

                count_tmp += c  # 個体の数をカウント

                if c == 1:
                    # 生存している場合、減衰量を推定する
                    theta = encode(c_gen)

                    qc = QuantumCircuit(2, 1)
                    qc.rx(theta, 0)
                    qc.ry(env_interaction_theta, 1)
                    qc.cx(0, 1)
                    qc.ry(-env_interaction_theta, 1)
                    qc.cx(0, 1)
                    qc.cx(1, 0)
                    qc.measure(0, 0)

                    backend = Aer.get_backend('qasm_simulator')
                    shots = shots
                    results = execute(qc, backend=backend, shots=shots).result()
                    exp_value = getExpectedValue(results.get_counts())[1]

                    # 生き残り
                    if exp_value > death_value:
                        next_state[i, j] = 1
                        next_state_gen[i, j] = exp_value
                    # 死亡
                    else:
                        next_state[i, j] = 0
                        next_state_gen[i, j] = 0

                else:
                    if neighbor_cell_sum in non_live:
                        next_state[i, j] = 0
                        next_state_gen[i, j] = 0
                    else:

                        # 創発判定
                        qc = QuantumCircuit(9, 1)
                        qc.rx(encode(nw_gen), 1)
                        qc.rx(encode(n_gen), 2)
                        qc.rx(encode(ne_gen), 3)
                        qc.rx(encode(w_gen), 4)
                        qc.rx(encode(e_gen), 5)
                        qc.rx(encode(sw_gen), 6)
                        qc.rx(encode(s_gen), 7)
                        qc.rx(encode(se_gen), 8)
                        qc.crx(live_theta, 1, 0)
                        qc.crx(live_theta, 2, 0)
                        qc.crx(live_theta, 3, 0)
                        qc.crx(live_theta, 4, 0)
                        qc.crx(live_theta, 5, 0)
                        qc.crx(live_theta, 6, 0)
                        qc.crx(live_theta, 7, 0)
                        qc.crx(live_theta, 8, 0)
                        qc.measure(0, 0)

                        backend = Aer.get_backend('qasm_simulator')
                        results = execute(qc, backend=backend, shots=shots).result()
                        exp_value = getExpectedValue(results.get_counts())[1]

                        # print(expValue)

                        # 創発判定
                        if live_low < exp_value < live_high:
                            next_state[i, j] = 1
                            next_state_gen[i, j] = 1
                        else:
                            next_state[i, j] = 0
                            next_state_gen[i, j] = 0

        state, next_state, state_gen, next_state_gen = next_state, state, next_state_gen, state_gen

        # 表示をアップデート
        visualizer.update(1 - state_gen)

        # 個体の数をセット
        out.append([loop, count_tmp])

        if data_file and loop >= data_num:
            df = pd.DataFrame(np.array(out), columns=['time_step', 'data'])
            outfile = data_file_name
            df.to_csv(outfile)
            visualizer.close()
            return df

    return
