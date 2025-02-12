import tkinter as tk
from tkinter import ttk
import math

# Function to calculate probabilities using a Poisson-like approximation
def poisson_probability(mean, k):
    return (math.exp(-mean) * (mean ** k)) / math.factorial(k)

def calculate_probabilities():
    try:
        avg_goals_home_scored = float(entry_home_scored.get())
        avg_goals_away_conceded = float(entry_away_conceded.get())
        avg_goals_away_scored = float(entry_away_scored.get())
        avg_goals_home_conceded = float(entry_home_conceded.get())
        injuries_home = int(entry_injuries_home.get())
        injuries_away = int(entry_injuries_away.get())
        position_home = int(entry_position_home.get())
        position_away = int(entry_position_away.get())
        form_home = int(entry_form_home.get())
        form_away = int(entry_form_away.get())
        bookmaker_odds_draw = float(entry_bookmaker_odds_draw.get())
        bookmaker_odds_under_2_5 = float(entry_bookmaker_odds_under_2_5.get())  # Renamed for clarity
        account_balance = float(entry_account_balance.get())

        # Adjust goal averages based on injuries, form, and league position
        adjusted_home_goals = avg_goals_home_scored * (1 - 0.05 * injuries_home) + form_home * 0.1 - position_home * 0.05
        adjusted_away_goals = avg_goals_away_scored * (1 - 0.05 * injuries_away) + form_away * 0.1 - position_away * 0.05

        # Predict score probabilities using Poisson approximation
        home_goals_probs = [poisson_probability(adjusted_home_goals, i) for i in range(5)]
        away_goals_probs = [poisson_probability(adjusted_away_goals, i) for i in range(5)]

        # Calculate the draw probability
        draw_probability = sum([home_goals_probs[i] * away_goals_probs[i] for i in range(5)])

        # **Increase weighting for common draw outcomes (0-0, 1-1, 2-2)**
        draw_probability += (home_goals_probs[0] * away_goals_probs[0]) * 0.15  # Extra 15% weight for 0-0
        draw_probability += (home_goals_probs[1] * away_goals_probs[1]) * 0.10  # Extra 10% weight for 1-1
        draw_probability += (home_goals_probs[2] * away_goals_probs[2]) * 0.05  # Extra 5% weight for 2-2

        # **Boost draw probability for evenly matched teams**
        if abs(position_home - position_away) <= 2:
            draw_probability *= 1.15  # Increase by 15%

        # **Properly adjust for Over/Under 2.5 Goals**
        implied_probability_under_2_5 = 1 / bookmaker_odds_under_2_5  # How likely Under 2.5 is
        adjustment_factor = 1 + (implied_probability_under_2_5 - 0.5)  # Adjust based on deviation

        # Ensure adjustment factor stays in a reasonable range (0.7 - 1.3)
        adjustment_factor = min(1.3, max(0.7, adjustment_factor))

        # **Apply the adjustment properly**
        adjusted_draw_probability = draw_probability * adjustment_factor

        # Calculate edge for laying strategy
        edge = (1 / bookmaker_odds_draw) - (1 / adjusted_draw_probability)

        # **New Kelly stake calculation (trigger at edge < -4.0)**
        if edge < -4.0:  # Changed from -7.0 to -4.0
            edge_magnitude = abs(edge + 4.0)  # Adjusted to match new threshold
            kelly_fraction = 0.025 * (edge_magnitude / 3)  # Reduced Kelly to 10%
            recommended_stake = kelly_fraction * account_balance
        else:
            recommended_stake = 0

        result_label["text"] = (f"Bookmaker Draw Odds: {bookmaker_odds_draw:.2f}\n"
                                f"Calculated Draw Odds (Adjusted): {1 / adjusted_draw_probability:.2f}\n"
                                f"Adjustment Factor (Under 2.5 Goals): {adjustment_factor:.4f}\n"
                                f"Edge: {edge:.4f}\n"
                                f"Recommended Stake: £{recommended_stake:.2f}")
    except ValueError:
        result_label["text"] = "Please enter valid numerical values."

# Function to reset all fields
def reset_fields():
    for entry in entries.values():
        entry.delete(0, tk.END)
    result_label["text"] = ""

# Create the main application window
root = tk.Tk()
root.title("Football Draw Prediction")

# Input fields
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
    ("Account Balance", "entry_account_balance"),
]

entries = {}

for i, (label_text, var_name) in enumerate(fields):
    label = tk.Label(root, text=label_text)
    label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

    entry = ttk.Entry(root)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries[var_name] = entry

# Assigning entries to variables for easier access
entry_home_scored = entries["entry_home_scored"]
entry_home_conceded = entries["entry_home_conceded"]
entry_away_scored = entries["entry_away_scored"]
entry_away_conceded = entries["entry_away_conceded"]
entry_injuries_home = entries["entry_injuries_home"]
entry_injuries_away = entries["entry_injuries_away"]
entry_position_home = entries["entry_position_home"]
entry_position_away = entries["entry_position_away"]
entry_form_home = entries["entry_form_home"]
entry_form_away = entries["entry_form_away"]
entry_bookmaker_odds_draw = entries["entry_bookmaker_odds_draw"]
entry_bookmaker_odds_under_2_5 = entries["entry_bookmaker_odds_under_2_5"]
entry_account_balance = entries["entry_account_balance"]

# Buttons
calculate_button = ttk.Button(root, text="Calculate Draw Probability", command=calculate_probabilities)
calculate_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

reset_button = ttk.Button(root, text="Reset Fields", command=reset_fields)
reset_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="", font=("Helvetica", 14))
result_label.grid(row=len(fields) + 2, column=0, columnspan=2, pady=10)

root.mainloop()
