import numpy as np

def run_model(
    demand_intercept: float = 240,
    demand_slope: float = 2,
    bearing_cost: float = 6,
    machine_cost: float = 4,
    bearings_per_machine: int = 2
):
    """
    Solves the vertical FDI model with separated firms.
    Returns equilibrium prices, quantities, and profits.
    """

        # -- Greek firm's reacting function -- #
        # Q = *236 - 2*P_b) / 4
    def greek_quantity(P_b):
        return (demand_intercept - machine_cost - bearings_per_machine * P_b) / (2 * demand_slope)

        # Slovenian profit as function of P_b -- #
    def slovenian_profit(P_b):
        Q = greek_quantity(P_b)
        q = bearings_per_machine * Q
        return (P_b * q) - (bearing_cost * q)
    
        # Solve Slovenian FOC analytically
        # From derivation: P_b = 60.5
    P_b_star = (demand_intercept - machine_cost) / 4

        # Equilibrium Quantities
    Q_star = greek_quantity(P_b_star)
    q_star = bearings_per_machine * Q_star

        # Market price of machines
    P_star = demand_intercept - demand_slope * Q_star

        # Profits
    pi_S = slovenian_profit(P_b_star)
    pi_G = (
        P_star * Q_star
        - machine_cost * Q_star
        - P_b_star * bearings_per_machine * Q_star
    )

    return {
        'ball_bearing price': P_b_star,
        'machine_price': P_star,
        'machines_quanity': Q_star,
        'bearings_quantity': q_star,
        'slovenian_profit': pi_S,
        'greek_profit': pi_G
    }