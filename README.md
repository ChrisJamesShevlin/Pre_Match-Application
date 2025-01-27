

---

# Football Draw Prediction Calculator

This Python application uses a Poisson-like approximation to calculate the probability of a draw in a football match. It takes into account various data points such as average goals scored, injuries, form, league positions, and bookmaker odds to provide a recommendation on betting strategy, including stake size using the Kelly Criterion.

## Features

- **Draw Probability Calculation**: Estimates the likelihood of a draw based on team statistics and form.
- **Poisson Approximation**: Uses a Poisson-like distribution to model goal-scoring probabilities.
- **Betting Strategy**: Calculates the edge between bookmaker odds and predicted odds, then uses the Kelly Criterion to suggest an optimal stake.
- **Graphical User Interface (GUI)**: Built with Tkinter, providing a user-friendly interface for input and result display.

## Requirements

- Python 3.x
- Tkinter (usually comes with Python)
- Math library (part of Python's standard library)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/football-draw-prediction.git
   ```
   
2. Navigate to the project folder:
   ```
   cd football-draw-prediction
   ```

3. Ensure Python 3.x is installed on your system, along with the Tkinter module. Tkinter is included by default with most Python distributions.

## Usage

1. Run the script:
   ```
   python football_draw_prediction.py
   ```
2. Enter the required data fields such as home team goals, away team injuries, bookmaker odds, and your account balance.
3. Press the "Calculate Draw Probability" button to see the result, including the draw probability, recommended stake, and betting edge.

---

