import numpy as np
import sympy as sp


def vertical_fdi_separated(
    demand_intercept: float = 240,
    demand_slope: float = 2,
    bearing_cost: float = 6,
    machine_cost: float = 4,
    bearings_per_machine: int = 2
):
    """
    Interactive Vertical FDI(Scenario 1: Separated Firms)
    Returns equilibrium prices, quantities, and profits.
    """

        # Returns the quantity of machines for Greek firm.
        # If Q_override is provided, use it; otherwise use profit-maximizing Q.
    def greek_quantity(P_b):
        return (demand_intercept - machine_cost - bearings_per_machine * P_b) / (2 * demand_slope)

        # Slovenian profit as function of P_b -- #
    def slovenian_profit(P_b):
        Q = greek_quantity(P_b)
        return (2 * P_b - bearing_cost) * Q  
    
    # --- Equilibrium Prices & Quantities --- #
    P_b_star = (demand_intercept - machine_cost + 0.5 * bearings_per_machine * bearing_cost) / (2 * bearings_per_machine) 


    Q_star = greek_quantity(P_b_star)
    Q_star = max(0, Q_star)
    q_star = bearings_per_machine * Q_star
    q_star = max(0, q_star)

    P_star = demand_intercept - demand_slope * Q_star
    P_star = max(0, P_star)
    # Profits
    pi_S = slovenian_profit(P_b_star)
    pi_G = (P_star * Q_star - machine_cost * Q_star - P_b_star * bearings_per_machine * Q_star)

    return {
        'ball_bearing_price': P_b_star,
        'machine_price': P_star,
        'machine_quantity': Q_star,
        'bearing_quantity': q_star,
        'upstream_profit': pi_S,
        'downstream_profit': pi_G
    }


def vertical_fdi_integrated(
        demand_intercept: float = 240,
        demand_slope: float = 2,
        bearing_cost: float = 6,
        machine_cost: float = 4, 
        bearings_per_machine: int = 2,
        fixed_cost: float = 1000
):
    """
    Vertically Integrated Firm.
    Returns prices, quantities and profits.
    """

    effective_downstream_cost = machine_cost + bearings_per_machine * bearing_cost

    Q_star = max(0, (demand_intercept - effective_downstream_cost) / (2 * demand_slope))

    P_star = max(0, demand_intercept - demand_slope * Q_star)

    q_star = bearings_per_machine * Q_star

    # Profits
    pi_I = P_star * Q_star - effective_downstream_cost * Q_star - fixed_cost

    return {
        'ball_bearing_price': bearing_cost,
        'machine_price': P_star,
        'machine_quantity': Q_star,
        'bearing_quantity': q_star,
        'integrated_profit': pi_I,
        'fixed_cost': fixed_cost
    }