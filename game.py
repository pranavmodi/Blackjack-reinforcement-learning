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
