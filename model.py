"""
Model functions for Vertical FDI Project
Author: Drew Lesh
Description: Implements separated and integrated equilibrium calculations
            and additional scenarios(transfer pricing, buying at cost).
"""


import numpy as np

DEFAULT_PARAMS_VFDI = {
    'cu': 6, # Upstream marginal cost
    'cd': 4, # Downstream marginal cost per machine
    'k': 2,  # Units of input per output (ball bearings per machine)
    'a': 240,  # Demand intercept
    'b': 2,  # Demand slope
    'fixed_cost': 1000  # Fixed cost for integration
}

# Separated Firms Equilibrium
def separated_equilibrium(cu=DEFAULT_PARAMS_VFDI['cu'], cd=DEFAULT_PARAMS_VFDI['cd'], k=DEFAULT_PARAMS_VFDI['k'], a=DEFAULT_PARAMS_VFDI['a'], b=DEFAULT_PARAMS_VFDI['b']):
    """
    Separated firm equilibrium (independent upstream & downstream monopololists)
    Returns eq. price, quantity, and profits under vertical separation.
    
    :param a: demand intercept (maximum willingness to pay / price at quantity 0)
    :param b: demand slope (amount price falls as quantity increases)
    :param cu: upstream marginal cost (cost to produce one unit of the input)
    :param cd: downstream marginal cost (cost to assemble one unit of the final good)
    :param k: input requirement (units of input needed per unit of output)
    """

    # Upstream price of input (ball bearings)
    pb = (a - cd + k*cu) / (2*k)

    # Downstream quantity
    Q = (a - cd - k*pb) / (2*b)

    # Final good price
    P = a - b*Q

    # Profits
    pi_down = (P - cd - k*pb) * Q
    pi_up = (pb - cu) * k * Q

    return {
        'Q': Q,
        'P': P,
        'pb': pb,
        'pi_down': pi_down,
        'pi_up': pi_up,
        'pi_total': pi_down + pi_up
    }


# Integrated Equilibrium (MNC)
def integrated_equilibrium(a=DEFAULT_PARAMS_VFDI['a'], b=DEFAULT_PARAMS_VFDI['b'], cu=DEFAULT_PARAMS_VFDI['cu'], cd=DEFAULT_PARAMS_VFDI['cd'], k=DEFAULT_PARAMS_VFDI['k']):
    """
    Equilibrium under vertical integration
    """
    # Profit-maximizing Quantity
    Q = (a - cd - k*cu) / (2*b)  # internalizes upstream cost k*cu, so no double marginalization

    # Equilibrium Price of final good
    P = a - b*Q

    # Profit 
    pi = (P - cd - k*cu) * Q - DEFAULT_PARAMS_VFDI['fixed_cost']

    return {
        "Q": Q,
        "P": P,
        "pi": pi
    }


# Transfer Pricing: set input price so upstream gets same profit as standalone
def transfer_pricing_equilibrium(target_pi_up, a=DEFAULT_PARAMS_VFDI['a'], b=DEFAULT_PARAMS_VFDI['b'],
                    cu=DEFAULT_PARAMS_VFDI['cu'], cd=DEFAULT_PARAMS_VFDI['cd'], k=DEFAULT_PARAMS_VFDI['k'], fixed_cost=DEFAULT_PARAMS_VFDI['fixed_cost']):
    
    """
    Calculate equilibrium under transfer pricing:
    Sets input price so that upstream earns a target profit
    (price bearing = profit level downstream as a separated firm).
    """
    # Solve for Pb from upstream profit target:
    # target_pi_up = (Pb - cu) * k * Q
    # Q = (a - cd - k*Pb) / (2*b)
    # Substitute Q and solve for Pb:

    pb = (2 * b * target_pi_up + k * cu * (a - cd)) / (k * (a - cd + k * cu))

    # Downstream quantity and price
    Q = (a - cd - k*pb)/(2*b)
    P = a - b * Q

    # Profits
    pi_down = (P - cd - k * pb) * Q
    pi_up = (pb - cu) * k * Q
    pi_total = pi_down + pi_up - fixed_cost
    return {'Q': Q, 'P': P, 'pb': pb, 'pi_down': pi_down, 'pi_up': pi_up, 'pi_total': pi_total}


# Buying at cost (downstream pays upstream marginal cost)
def buy_at_cost_equilibrium(a=DEFAULT_PARAMS_VFDI['a'], b=DEFAULT_PARAMS_VFDI['b'], cu=DEFAULT_PARAMS_VFDI['cu'], cd=DEFAULT_PARAMS_VFDI['cd'], k=DEFAULT_PARAMS_VFDI['k'], fixed_cost=DEFAULT_PARAMS_VFDI['fixed_cost']):
    # pay upstream marginal cost
    pb = cu 

    # Effective marginal cost of a machine
    MC = cd + k * pb

    # Monopoly outcome
    Q = (a - MC) / ( 2 * b )
    P = a - b * Q

    # Profits
    pi_down = (P - MC) * Q
    pi_up = (pb - cu) * k * Q # no upstream profit at cost
    pi_total = pi_down + pi_up - fixed_cost
    return {'Q': Q, 'P': P, 'pb': pb, 'pi_down': pi_down, 'pi_up': pi_up, 'pi_total': pi_total}


DEFAULT_PARAMS_HFDI = {
    'a_ire': 280,   # Demand intercept Ireland
    'a_eng': 400,   # Demand Intercept England
    'b_ire': 1,     # Demand slope Ireland (linear)
    'b_eng': 1,     # Demand slope England (linear)
    'F': 8000,      # Fixed cost per active plant
    'c_ire': None,  # Ireland production cost per unit(Y**2)
    'c_eng': None,  # England prod. cost per unit (Z**2)
    't': 20         # Transport cost per unit exported
}

# Horizontal Foregin Direct Investment - Only exporting from Home Country
def export_only(a_ire=DEFAULT_PARAMS_HFDI['a_ire'], 
                               a_eng=DEFAULT_PARAMS_HFDI['a_eng'],
                               b_ire=DEFAULT_PARAMS_HFDI['b_ire'],
                               b_eng=DEFAULT_PARAMS_HFDI['b_eng'],
                               F=DEFAULT_PARAMS_HFDI['F'],
                               t=DEFAULT_PARAMS_HFDI['t']):
    """
    Compute Equilibrium quantities, prices, and profit for Export-only scenarios
    """

    # Set up the linear system from first-order conditions
    # Q = quantity sold in Ireland
    # Q_star = quantity sold in England
    # Equations:
    # Ireland: a_ie - 2*Q - 2*Q_star = 0
    # England: a_en - 2*Q_star - 2*Q - t = 0

    # Coefficient mattrix for linear system
    A = np.array([[4, 2],
                  [2, 4]])
    b_vec = np.array([a_ire, a_eng - t])

    # Solve linear system
    Q, Q_star = np.linalg.solve(A, b_vec)

    # Prices
    P_ie = a_ire - Q
    P_en = a_eng - Q_star

    # Total revenue
    TR = P_ie * Q + P_en * Q_star

    # Total cost: production + transportation + fixed cost
    TC = (Q + Q_star) * Q_star + t * Q_star + F

    profit = TR - TC

    return {
        'Q_ie': float(Q),
        'Q_en': float(Q_star),
        'P_ie': float(P_ie),
        'P_en': float(P_en),
        'profit': float(profit)
    }


# Equilibriums model for horizontal FDI
def horizontal_FDI(Y=None, Z=None, X=None,
                          a_ire=DEFAULT_PARAMS_HFDI['a_ire'],
                          a_eng=DEFAULT_PARAMS_HFDI['a_eng'],
                          transport_cost=DEFAULT_PARAMS_HFDI['t'],
                          fixed_cost=DEFAULT_PARAMS_HFDI['F']):
    """
    Calculates equilibrium for a two-plant(horizontal FDI) scenario.

    :param Y: Production in Ireland
    :param Z: Production in England
    :param X: Export from Ireland to England
    """

    # use derived equilibriums
    X = 20
    Y = 70
    Z = 100

    Q_ireland = Y - X
    Q_england = Z + X

    P_ireland = a_ire - Q_ireland
    P_england = a_eng - Q_england

    TR = P_ireland * Q_ireland + P_england * Q_england
    TC = Y**2 + Z**2 + transport_cost * X + 2 * fixed_cost
    
    profit = TR - TC

    return {
        'Y_ireland': Y,
        'Z_england': Z,
        'X_export': X,
        'Q_ireland': Q_ireland,
        'Q_england': Q_england,
        'P_ireland': P_ireland,
        'P_england': P_england,
        'TR': TR,
        'TC': TC,
        'profit': profit
    }