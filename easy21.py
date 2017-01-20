import os
import numpy as np
import fileinput
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


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


def agent_action(state, sa_value, ep):
    ## 0 == 's', 1 == 'h'
    v1, v2 = sa_value[state[0]-1, state[1]-1, :]
    r = np.random.rand(1)[0]
    if r > ep:
        if v1 > v2:
            return 0
        else:
            return 1
    else:
        return np.random.randint(0,2)

def ep_greedy_reward(state, ep):
    v1, v2 = state
    if v1 > v2:
        return ep*v2 + (1 - ep)*v1
    else:
        return ep*v1 + (1 - ep)*v2

def start_games(num_games):

    sa_value = np.zeros((10,21,2))
    sa_counts = np.zeros((10,21,2))
    wins = 0
    losses = 0
    draws = 0
    n0 = np.float32(100000)
    for i in range(num_games):
        ep = n0/(n0 + i)

        if i % 100000 == 0:
            if i > 0:
                print np.float32(wins)/(wins + losses + draws), ep
                wins = 0
                losses = 0
                draws = 0
            print 'Playing game number: ', i

        dealer_draw = draw_till_black()
        player_draw = draw_till_black()
        player_score = player_draw[1]
        dealer_fc = dealer_draw[1]
        state = [dealer_fc, player_score, 'NT']
        reward = 0
        while state[2] != 'T':
            ds, ps, tnt = state
            action = agent_action(state, sa_value, ep)
            v = sa_value[state[0]-1, state[1]-1, action]
            sa_counts[state[0]-1, state[1]-1, action] += 1
            c = sa_counts[state[0]-1, state[1]-1, action]
            new_state, reward = step(state, action)
            if new_state[2] == 'T':
                v = v + (reward - v)/c
                sa_value[state[0]-1, state[1]-1, action] = v
            else:
                r_pair = sa_value[new_state[0]-1, new_state[1]-1, :]
                new_state_val = reward + ep_greedy_reward(r_pair, ep)
                old_state_val = sa_value[state[0]-1, state[1]-1, action]
                sa_value[state[0]-1, state[1]-1, action] = old_state_val + (new_state_val - old_state_val)/c
            state = new_state

        if reward == 1:
            wins += 1
        elif reward == -1:
            losses += 1
        else:
            draws += 1
    print 'wins losses: ', wins, losses
    return sa_value, sa_counts



if __name__ == "__main__":
    sa_value, sa_counts = start_games(1000)
