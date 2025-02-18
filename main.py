import tkinter as tk
from tkinter import ttk
import math

def poisson_probability(mean, k):
    return (math.exp(-mean) * (mean ** k)) / math.factorial(k)

def calculate_probabilities():
    try:
        avg_goals_home_scored = float(entries["entry_home_scored"].get())
        avg_goals_away_conceded = float(entries["entry_away_conceded"].get())
        avg_goals_away_scored = float(entries["entry_away_scored"].get())
        avg_goals_home_conceded = float(entries["entry_home_conceded"].get())
        injuries_home = int(entries["entry_injuries_home"].get())
        injuries_away = int(entries["entry_injuries_away"].get())
        position_home = int(entries["entry_position_home"].get())
        position_away = int(entries["entry_position_away"].get())
        form_home = int(entries["entry_form_home"].get())
        form_away = int(entries["entry_form_away"].get())
        bookmaker_odds_draw = float(entries["entry_bookmaker_odds_draw"].get())
        bookmaker_odds_under_2_5 = float(entries["entry_bookmaker_odds_under_2_5"].get())
        bookmaker_odds_home = float(entries["entry_bookmaker_odds_home"].get())
        bookmaker_odds_away = float(entries["entry_bookmaker_odds_away"].get())

        adjusted_home_goals = avg_goals_home_scored * (1 - 0.05 * injuries_home) + form_home * 0.1 - position_home * 0.05
        adjusted_away_goals = avg_goals_away_scored * (1 - 0.05 * injuries_away) + form_away * 0.1 - position_away * 0.05

        goal_range = 10
        home_goals_probs = [poisson_probability(adjusted_home_goals, i) for i in range(goal_range)]
        away_goals_probs = [poisson_probability(adjusted_away_goals, i) for i in range(goal_range)]

        draw_probability = sum([home_goals_probs[i] * away_goals_probs[i] for i in range(goal_range)])
        home_win_probability = sum([sum(home_goals_probs[i] * away_goals_probs[j] for j in range(i)) for i in range(goal_range)])
        away_win_probability = sum([sum(home_goals_probs[j] * away_goals_probs[i] for j in range(i)) for i in range(goal_range)])

        total_prob = home_win_probability + away_win_probability + draw_probability
        home_win_probability /= total_prob
        away_win_probability /= total_prob
        draw_probability /= total_prob

        draw_adjustment_factor = 1.10 if bookmaker_odds_draw < 3 else 0.90
        draw_probability *= draw_adjustment_factor

        calculated_draw_odds = (1 / draw_probability + bookmaker_odds_draw) / 2
        calculated_home_odds = (1 / home_win_probability + bookmaker_odds_home) / 2
        calculated_away_odds = (1 / away_win_probability + bookmaker_odds_away) / 2

        edge_draw = (draw_probability - (1 / bookmaker_odds_draw)) / (1 / bookmaker_odds_draw)
        edge_home = (home_win_probability - (1 / bookmaker_odds_home)) / (1 / bookmaker_odds_home)
        edge_away = (away_win_probability - (1 / bookmaker_odds_away)) / (1 / bookmaker_odds_away)

        # Fix: Include draw in lay bet selection
        layable_edges = {
            "home": edge_home if bookmaker_odds_home < calculated_home_odds else float('inf'),
            "away": edge_away if bookmaker_odds_away < calculated_away_odds else float('inf'),
            "draw": edge_draw if bookmaker_odds_draw < calculated_draw_odds else float('inf')  # Corrected
        }

        # Select the most negative edge (strongest lay bet)
        biggest_edge_outcome = min(layable_edges, key=lambda k: layable_edges[k])

        if layable_edges[biggest_edge_outcome] == float('inf'):
            biggest_edge_outcome = "No suitable lay bet"
            biggest_edge_value = 0
        else:
            biggest_edge_value = layable_edges[biggest_edge_outcome]

        # Print debugging info
        print(f"Bookmaker Home: {bookmaker_odds_home}, Calculated: {calculated_home_odds}, Edge: {edge_home}")
        print(f"Bookmaker Away: {bookmaker_odds_away}, Calculated: {calculated_away_odds}, Edge: {edge_away}")
        print(f"Bookmaker Draw: {bookmaker_odds_draw}, Calculated: {calculated_draw_odds}, Edge: {edge_draw}")
        print(f"Biggest Edge: {biggest_edge_outcome} with Edge: {biggest_edge_value}")

        # Update UI
        result_label["text"] = (f"Bookmaker Home: {bookmaker_odds_home:.2f}, Calculated: {calculated_home_odds:.2f}, Edge: {edge_home:.4f}\n"
                                f"Bookmaker Away: {bookmaker_odds_away:.2f}, Calculated: {calculated_away_odds:.2f}, Edge: {edge_away:.4f}\n"
                                f"Bookmaker Draw: {bookmaker_odds_draw:.2f}, Calculated: {calculated_draw_odds:.2f}, Edge: {edge_draw:.4f}\n"
                                f"Biggest Edge: {biggest_edge_outcome} with Edge: {biggest_edge_value:.4f}")
    except ValueError:
        result_label["text"] = "Please enter valid numerical values."

def reset_fields():
    for entry in entries.values():
        entry.delete(0, tk.END)
    result_label["text"] = ""

root = tk.Tk()
root.title("Football Betting Value Analysis")

fields = [
    ("Home Team Average Goals Scored", "entry_home_scored"),
    ("Home Team Average Goals Conceded", "entry_home_conceded"),
    ("Away Team Average Goals Scored", "entry_away_scored"),
    ("Away Team Average Goals Conceded", "entry_away_conceded"),
    ("Home Team Injuries", "entry_injuries_home"),
    ("Away Team Injuries", "entry_injuries_away"),
    ("Home Team League Position", "entry_position_home"),
    ("Away Team League Position", "entry_position_away"),
    ("Home Team Wins in Last 5 Matches", "entry_form_home"),
    ("Away Team Wins in Last 5 Matches", "entry_form_away"),
    ("Bookmaker Offered Draw Odds", "entry_bookmaker_odds_draw"),
    ("Bookmaker Odds for Under 2.5 Goals", "entry_bookmaker_odds_under_2_5"),
    ("Bookmaker Odds for Home Win", "entry_bookmaker_odds_home"),
    ("Bookmaker Odds for Away Win", "entry_bookmaker_odds_away"),
]

entries = {}
for i, (label_text, var_name) in enumerate(fields):
    label = tk.Label(root, text=label_text)
    label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
    entry = ttk.Entry(root)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries[var_name] = entry

button_frame = tk.Frame(root)
button_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)

calculate_button = ttk.Button(button_frame, text="Calculate Betting Value", command=calculate_probabilities)
calculate_button.grid(row=0, column=0, padx=5)

reset_button = ttk.Button(button_frame, text="Reset", command=reset_fields)
reset_button.grid(row=0, column=1, padx=5)

result_label = tk.Label(root, text="", font=("Helvetica", 14))
result_label.grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)

root.mainloop()
