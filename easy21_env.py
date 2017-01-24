import os
import numpy as np
import fileinput
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from agent import agent_action


def draw_till_black():
    color = 3
    while color == 3:
        color = np.random.randint(1,4)
        num = np.random.randint(1,11)
    return color, num

def calculate_score(draws):
    black_draws = [d for d in draws if d[0] != 3]
    red_draws = [d for d in draws if d[0] == 3]
    black_sum = reduce(lambda s, x: x[1] + s, black_draws, 0)
    red_sum = reduce(lambda s, x: x[1] + s, red_draws, 0)
    return black_sum - red_sum


def draw_dealer_cards(dealer_score):
    while dealer_score > 0 and dealer_score < 17:
        draw_num = np.random.randint(1,11)
        draw_color = np.random.randint(1,4)
        if draw_color == 3:
            dealer_score -= draw_num
        else:
            dealer_score += draw_num
    return dealer_score


def step(state, action):
    new_state = state
    if action == 0:
        new_state[2] = 'T'
        player_score = state[1]
        dealer_score = draw_dealer_cards(state[0])
        if dealer_score < 1 or dealer_score > 21:
            return (new_state, 1)
        if dealer_score > player_score:
            return (new_state, -1)
        elif dealer_score == player_score:
            return (new_state, 0)
        else:
            return (new_state, 1)

    if action == 1:
        draw_num = np.random.randint(1,11)
        draw_color = np.random.randint(1,4)
        player_score = state[1]
        if draw_color == 3:
            player_score -= draw_num
        else:
            player_score += draw_num
        state[1] = player_score
        if player_score > 21 or player_score < 1:
            state[2] = 'T'
            state[1] = player_score - draw_num
            return state, -1
        reward = 0
    return state, reward


def ep_greedy_reward(state, ep):
    v1, v2 = state
    if v1 > v2:
        return ep*v2 + (1 - ep)*v1
    else:
        return ep*v1 + (1 - ep)*v2


