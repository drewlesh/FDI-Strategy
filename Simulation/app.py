import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from model import vertical_fdi_separated, vertical_fdi_integrated

st.title('Vertical FDI Simulation - Separated Firms')

a = st.slider("Demand Intercept (a)", 100, 500, 240)
b = st.slider("Demand Slope (b)", 1, 10, 2, 1)
c_u = st.slider("Upstream Cost (Ball Bearings)", 1, 20, 6, 1)
c_d = st.slider('Downstream Cost (Machines)', 1, 20, 4, 1)
k = st.slider('Bearings per Machine', 1, 20, 2, 1)
fc = st.slider('Fixed Cost', 0, 5000, 1000, 100)


sep_results = vertical_fdi_separated(
    demand_intercept=a,
    demand_slope=b,
    bearing_cost=c_u,
    machine_cost=c_d,
    bearings_per_machine=k
)

int_results = vertical_fdi_integrated(
    demand_intercept=a,
    demand_slope=b,
    bearing_cost=c_u,
    machine_cost=c_d,
    bearings_per_machine=k,
    fixed_cost=fc
)



st.subheader('Equilibrium Outcomes')

# Separated Firms Outcomes
st.write(f"Ball Bearing Price: {sep_results['ball_bearing_price']: .2f}")
st.write(f"Ball Bearing Quantity: {sep_results['bearing_quantity']: .2f}")
st.write(f"Machine Price: {sep_results['machine_price']: .2f}")
st.write(f"Machine Quantity: {sep_results['machine_quantity']: .2f}")
st.write(f"Upstream Profit: {sep_results['upstream_profit']: .2f}")
st.write(f"Downstream Profit: {sep_results['downstream_profit']: .2f}")

# Integrated Firms Outcomes:
st.write(f"Ball Bearing Price: {int_results['ball_bearing_price']: .2f}")
st.write(f"Ball Bearing Quantity: {int_results['bearing_quantity']: .2f}")
st.write(f"Machine Price: {int_results['machine_price']: .2f}")
st.write(f"Machine Quantity: {int_results['machine_quantity']: .2f}")
st.write(f"integrated Profit: {int_results['integrated_profit']: .2f}")


# --- Profit vs Ball Bearing Price Graph --- #
Pb_max = 200
Pb_vals = np.linspace(0, Pb_max, 300)

# Separated Firm Profits
pi_S_vals, pi_G_vals = [], []
for Pb in Pb_vals:
    Q_temp = max(0, (a - c_d - k*Pb)/(2*b))
    P_temp = max(0, a - b*Q_temp)
    pi_S_vals.append(max(0, (2*Pb - c_u)*Q_temp))
    pi_G_vals.append(max(0, P_temp*Q_temp - c_d*Q_temp - Pb*k*Q_temp))

pi_I_vals = [int_results['integrated_profit']] * len(Pb_vals)

# --- Plot --- #

fig = go.Figure()
fig.add_trace(go.Scatter(x=Pb_vals, y=pi_S_vals, mode='lines', name='Upstream Profit (Separated)', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=Pb_vals, y=pi_G_vals, mode='lines', name='Downstream Profit (Separated)', line=dict(color='green')))
fig.add_trace(go.Scatter(x=Pb_vals, y=pi_I_vals, mode='lines', name='Integrated Profit', line=dict(color='red', dash='dash')))

# Equilibrium lines
fig.add_vline(x=sep_results['ball_bearing_price'], line=dict(color='gray', dash='dot'), annotation_text="Sep Pb")
fig.add_vline(x=int_results['ball_bearing_price'], line=dict(color='black', dash='dot'), annotation_text="Int Pb")

fig.update_layout(title="Profit vs Ball Bearing Price",
                  xaxis_title="Ball Bearing Price",
                  yaxis_title="Profit",
                  template="plotly_white")

st.plotly_chart(fig, use_container_width=True)