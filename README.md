
### `model.py`
Contains all analytical model functions used across the notebooks, including:

- Separated monopolists (double marginalization)
- Vertical integration (multinational firm)
- Transfer pricing
- Buy-at-cost input pricing
- Export-only and two-plant (horizontal FDI) equilibria

This file centralizes the economic logic and allows the notebooks to focus on analysis and visualization.

---

### `verticalFDI.ipynb`
Analyzes **vertical integration** in a supply chain:

- Upstream supplier produces intermediate inputs
- Downstream firm produces a final good
- Linear demand for the final good

Scenarios compared:

- Separated firms (double marginalization)
- Vertical integration
- Transfer pricing
- Buying inputs at marginal cost

Key concepts illustrated:

- Double marginalization
- Profit shifting vs. efficiency
- Effects of integration on prices, quantities, and welfare

---

### `horizontalFDI.ipynb`
Analyzes **horizontal FDI** decisions for a multinational firm serving two countries:

- Export-only production from the home country
- Two-plant production (local production in both markets)

Key trade-offs studied:

- Per-unit trade costs vs. fixed costs of foreign production
- Market size and optimal plant location
- Output allocation across countries

The notebook includes:

- Closed-form equilibrium solutions
- Profit comparisons across regimes
- Visualizations of quantities, prices, and profits

---

## Key Economic Insights

- Vertical integration eliminates double marginalization and increases total surplus.
- Transfer pricing and buy-at-cost arrangements affect **profit allocation**, not efficiency.
- Horizontal FDI is optimal when trade costs are high and foreign demand is sufficiently large.
- Fixed costs determine whether local production dominates exporting.

---

## Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib
- Jupyter Notebooks

---

## Background & Motivation

This project was developed as part of an advanced international economics coursework(University of Oregon) and extended into a structured, reusable modeling framework.  
It demonstrates how theoretical IO and trade models can be implemented, simulated, and visualized programmatically.

---

## Future Extensions

Potential extensions include:

- Welfare analysis (consumer surplus, total surplus)
- Comparative statics over trade and fixed costs
- Strategic interaction between multiple firms
- Empirical calibration

---

## Author

**Drew Lesh**
