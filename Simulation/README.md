# Vertical FDI Simulation

This is an interactive Streamlit app that simulates vertical foreign direct investment (FDI) scenarios with separated firms and integrated multinational corporations (MNCs). Users can explore how upstream and downstream costs, demand, and other parameters affect equilibrium prices, quantities, and profits.

## Features

- Adjustable sliders for:
  - Demand intercept and slope
  - Upstream (ball bearing) cost
  - Downstream (machine) cost
  - Bearings per machine
  - Fixed cost (for integrated MNC)
- Side-by-side comparison of:
  - Separated firms
  - Integrated MNC
- Interactive profit vs. ball bearing price graphs
- Dynamic LaTeX-rendered profit functions
- Equilibrium prices and profits displayed for both scenarios

## How to Run

1. Clone this repository:
   ```bash
   git clone <repo-url>
   cd <repo-folder>

2. Install Dependencies:
pip install -r requirements.txt

3. Run app through local folder(terminal prompt)
streamlit run app.py

