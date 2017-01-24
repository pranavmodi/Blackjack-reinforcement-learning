import numpy as np

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
