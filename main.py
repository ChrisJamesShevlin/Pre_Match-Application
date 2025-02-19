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

        # ✅ Improved Expected Goals Calculation (Now Includes Goals Conceded)
        adjusted_home_goals = ((avg_goals_home_scored + avg_goals_away_conceded) / 2) * (1 - 0.05 * injuries_home) + form_home * 0.1 - position_home * 0.02
        adjusted_away_goals = ((avg_goals_away_scored + avg_goals_home_conceded) / 2) * (1 - 0.05 * injuries_away) + form_away * 0.1 - position_away * 0.02

        goal_range = 10
        home_goals_probs = [poisson_probability(adjusted_home_goals, i) for i in range(goal_range)]
        away_goals_probs = [poisson_probability(adjusted_away_goals, i) for i in range(goal_range)]

        draw_probability = sum([home_goals_probs[i] * away_goals_probs[i] for i in range(goal_range)])
        home_win_probability = sum([sum(home_goals_probs[i] * away_goals_probs[j] for j in range(i)) for i in range(goal_range)])
        away_win_probability = sum([sum(home_goals_probs[j] * away_goals_probs[i] for j in range(i)) for i in range(goal_range)])

        # ✅ Normalize Probabilities (Ensure They Sum to 100%)
        total_prob = home_win_probability + away_win_probability + draw_probability
        if total_prob > 0:
            home_win_probability /= total_prob
            away_win_probability /= total_prob
            draw_probability /= total_prob

        # ✅ Adjust Draw Probability (Prevent Overinflation)
        draw_adjustment_factor = 1 - (0.1 * (2.0 - bookmaker_odds_under_2_5)) if bookmaker_odds_under_2_5 < 2.0 else 1
        draw_adjustment_factor = max(0.85, draw_adjustment_factor)  # Prevent over-adjustment
        draw_probability *= draw_adjustment_factor

        # ✅ Normalize Again After Adjustment
        total_prob = home_win_probability + away_win_probability + draw_probability
        if total_prob > 0:
            home_win_probability /= total_prob
            away_win_probability /= total_prob
            draw_probability /= total_prob

        # ✅ Fair Odds Calculation (Based on Adjusted Probabilities)
        calculated_draw_odds = 1 / draw_probability
        calculated_home_odds = 1 / home_win_probability
        calculated_away_odds = 1 / away_win_probability

        # ✅ Edge Calculation (Difference Between Fair & Bookmaker Odds)
        edge_draw = (draw_probability - (1 / bookmaker_odds_draw)) / (1 / bookmaker_odds_draw)
        edge_home = (home_win_probability - (1 / bookmaker_odds_home)) / (1 / bookmaker_odds_home)
        edge_away = (away_win_probability - (1 / bookmaker_odds_away)) / (1 / bookmaker_odds_away)

        # ✅ Determine Best Lay Bet (Only If Bookmaker Odds Are Lower Than Fair Odds)
        layable_edges = {
            "home": edge_home if bookmaker_odds_home < calculated_home_odds else float('inf'),
            "away": edge_away if bookmaker_odds_away < calculated_away_odds else float('inf'),
            "draw": edge_draw if bookmaker_odds_draw < calculated_draw_odds else float('inf')
        }
        min_lay_edge_outcome = min(layable_edges, key=lambda k: layable_edges[k])
        biggest_edge_value = layable_edges[min_lay_edge_outcome]

        # ✅ Debugging Output
        print(f"Bookmaker Home: {bookmaker_odds_home}, Calculated: {calculated_home_odds:.2f}, Edge: {edge_home:.4f}")
        print(f"Bookmaker Away: {bookmaker_odds_away}, Calculated: {calculated_away_odds:.2f}, Edge: {edge_away:.4f}")
        print(f"Bookmaker Draw: {bookmaker_odds_draw}, Calculated: {calculated_draw_odds:.2f}, Edge: {edge_draw:.4f}")
        print(f"Biggest Edge: {min_lay_edge_outcome} with Edge: {biggest_edge_value:.4f}")

        # ✅ UI Update
        result_label["text"] = (f"Bookmaker Home: {bookmaker_odds_home:.2f}, Calculated: {calculated_home_odds:.2f}, Edge: {edge_home:.4f}\n"
                                f"Bookmaker Away: {bookmaker_odds_away:.2f}, Calculated: {calculated_away_odds:.2f}, Edge: {edge_away:.4f}\n"
                                f"Bookmaker Draw: {bookmaker_odds_draw:.2f}, Calculated: {calculated_draw_odds:.2f}, Edge: {edge_draw:.4f}\n"
                                f"Biggest Edge: {min_lay_edge_outcome} with Edge: {biggest_edge_value:.4f}")
    except ValueError:
        result_label["text"] = "Please enter valid numerical values."

root = tk.Tk()
root.title("Football Betting Value Analysis")

# Define the entries dictionary and create the entry widgets
entries = {
    "entry_home_scored": tk.Entry(root),
    "entry_away_conceded": tk.Entry(root),
    "entry_away_scored": tk.Entry(root),
    "entry_home_conceded": tk.Entry(root),
    "entry_injuries_home": tk.Entry(root),
    "entry_injuries_away": tk.Entry(root),
    "entry_position_home": tk.Entry(root),
    "entry_position_away": tk.Entry(root),
    "entry_form_home": tk.Entry(root),
    "entry_form_away": tk.Entry(root),
    "entry_bookmaker_odds_draw": tk.Entry(root),
    "entry_bookmaker_odds_under_2_5": tk.Entry(root),
    "entry_bookmaker_odds_home": tk.Entry(root),
    "entry_bookmaker_odds_away": tk.Entry(root),
}

# Create labels and place entry widgets
labels_text = [
    "Average Goals Home Scored", "Average Goals Away Conceded", "Average Goals Away Scored",
    "Average Goals Home Conceded", "Injuries Home", "Injuries Away", "Position Home",
    "Position Away", "Form Home", "Form Away", "Bookmaker Odds Draw",
    "Bookmaker Odds Under 2.5", "Bookmaker Odds Home", "Bookmaker Odds Away"
]

for i, (key, label_text) in enumerate(zip(entries.keys(), labels_text)):
    label = tk.Label(root, text=label_text)
    label.grid(row=i, column=0, padx=5, pady=5, sticky="e")
    entries[key].grid(row=i, column=1, padx=5, pady=5)

# Create and place the result label
result_label = tk.Label(root, text="", justify="left")
result_label.grid(row=len(entries), column=0, columnspan=2, padx=5, pady=5)

# Create and place the calculate button
calculate_button = tk.Button(root, text="Calculate Probabilities", command=calculate_probabilities)
calculate_button.grid(row=len(entries) + 1, column=0, columnspan=2, padx=5, pady=10)

root.mainloop()
