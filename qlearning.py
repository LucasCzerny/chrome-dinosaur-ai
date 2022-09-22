import dinosaur

from collections import defaultdict
import random

reward_alive = 1
reward_dead = -10000
alpha = 0.1
gamma = 1

Q = defaultdict(lambda: [0, 0])
old_state = None
old_action = None

highscore = 0
game_counter = 0

def should_emulate_key_press(params):
    global old_state, old_action

    state = params_to_state(params)
    estimated_reward = Q[state]

    index = 0
    if old_action:
        index = 1
    
    prev_reward = Q[old_state]
    prev_reward[index] = (1 - alpha) * prev_reward[index] + \
        alpha * (reward_alive + gamma * max(estimated_reward))

    Q[old_state] = prev_reward
    old_state = state

    if estimated_reward[0] >= estimated_reward[1]:
        old_action = False
        return False

    old_action = True
    return True
    
def on_gameover(game_highscore):
    global Q, old_state, old_action, game_counter, highscore

    game_counter += 1

    index = 1 if old_action else 0

    prev_reward = Q[old_state]
    prev_reward[index] = (1 - alpha) * prev_reward[index] + alpha * reward_dead

    Q[old_state] = prev_reward

    old_state, old_action = None, None

    if game_highscore > highscore:
        highscore = game_highscore
        print("Game #%s: %s" % (game_counter, highscore))

def params_to_state(params):
    cacti = list(params[0])
    birds = list(params[1])

    distances = []
    if len(cacti) != 0:
        distances.append(cacti[0].rect.left)
    elif len(cacti) > 1:
        distances.append(cacti[1].rect.left)
    else:
        distances.append(-1)
    
    if len(birds) != 0:
        distances.append(birds[0].rect.left)
    elif len(birds) > 1:
        distances.append(birds[1].rect.left)
    else:
        distances.append(-1)
    
    state = 0

    while state <= 0:
        if len(distances):
            state = distances.pop(distances.index(min(distances)))
        else: return -1

    state = round((state / 5) * 5)

    print(state)
    return state

dinosaur.main(should_emulate_key_press, on_gameover)