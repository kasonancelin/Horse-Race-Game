import itertools
import random
import pickle
import os

race_len = int(input("Enter the length of the race (default is 5): "))

def take_step(pos, card, back_card, flipped_idx):
    pos[card] += 1
    if pos[card] == race_len:  # Game is over, return index of winner
        return card, flipped_idx
    if all([val > flipped_idx for val in pos]):  # First time a backwards card is flipped
        pos[back_card] -= 1
        flipped_idx += 1  # Increment flipped as this level has already been flipped
    return -1, flipped_idx

def race(pos=[0] * 4):  # Outputs the winner as a number
    deck = [0, 1, 2, 3] * 12  # Does not include the 4 racers
    random.shuffle(deck)
    out = -1
    flipped_idx = 1
    while out == -1:
        out, flipped_idx = take_step(pos, deck.pop(), deck[-flipped_idx], flipped_idx)
    return out

def generate_unordered_lists(n):
    return [list(c) for c in itertools.combinations_with_replacement(range(n), 4)]

def compute_probabilities(race_len):
    pos_ls = generate_unordered_lists(race_len)
    prob_matrix = [[0] * 4 for _ in range(len(pos_ls))]
    for i, pos in enumerate(pos_ls):
        cur_pos = pos.copy()
        wins_ls = [0] * 4
        for _ in range(100000):
            wins_ls[race(pos)] += 1
            pos = cur_pos.copy()
        prob_matrix[i] = [x / 100000 for x in wins_ls]
    return pos_ls, prob_matrix

def save_probabilities(race_len, pos_ls, prob_matrix):
    filename = f"probabilities_race_len_{race_len}.pkl"
    with open(filename, "wb") as f:
        pickle.dump((pos_ls, prob_matrix), f)
    print(f"Probabilities saved to {filename}.")

def load_probabilities(race_len):
    filename = f"probabilities_race_len_{race_len}.pkl"
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            pos_ls, prob_matrix = pickle.load(f)
        print(f"Loaded precomputed probabilities from {filename}.")
        return pos_ls, prob_matrix
    else:
        print(f"No precomputed probabilities found for race length {race_len}. Computing now...")
        pos_ls, prob_matrix = compute_probabilities(race_len)
        save_probabilities(race_len, pos_ls, prob_matrix)
        return pos_ls, prob_matrix

# Load or compute probabilities
_, prob_matrix = load_probabilities(race_len) # They call me the full stack developer
# pos_ls WILL GET CHANGED OVER TIME AND CAN MESS UP state_to_probs function DURING LOOKUP

def state_to_probs(state, states_ls):  # State is a list of ints
    input_board = list(enumerate(state))
    sorted_input_board = sorted(input_board, key=lambda item: item[1])
    probs = prob_matrix[states_ls.index(sorted(state))]

    true_positional_probs = [0] * 4
    for i, prob in enumerate(probs):
        true_positional_probs[sorted_input_board[i][0]] = prob
    return true_positional_probs

def probs_to_prices(probs):
    return [val * 4 for val in probs]

def state_to_prices(state, state_ls):
    return probs_to_prices(state_to_probs(state, state_ls))

def state_to_perturbed_prices(state, state_ls):
    prices = probs_to_prices(state_to_probs(state, state_ls))
    return [max(0, price + random.gauss(0, 0.02 + price * 0.05)) for price in prices]

def calculate_prices(input_state):
    try:
        state = list(map(int, input_state.split()))
        POS_LS = generate_unordered_lists(race_len)
        return state_to_perturbed_prices(state, POS_LS)
    except ValueError:
        raise ValueError("Invalid input. Please enter valid integers separated by spaces.")

if __name__ == "__main__":
    print("Horse Race Probabilities and Prices")
    input_state = input("Enter board state (e.g., 0 1 2 1): ")
    try:
        prices = calculate_prices(input_state)
        print("Calculated Prices:", prices)
    except ValueError as e:
        print(f"Error: {e}")