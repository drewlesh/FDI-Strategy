import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from model import vertical_fdi_separated

st.title('Vertical FDI Simulation - Separated Firms')

a = st.slider("Demand Intercept (a)", 100, 500, 240)
b = st.slider("Demand Slope (b)", 1, 10, 2, 1)
c_u = st.slider("Upstream Cost (Ball Bearings)", 1, 20, 6, 1)
c_d = st.slider('Downstream Cost (Machines)', 1, 20, 4, 1)
k = st.slider('Bearings per Machine', 1, 20, 2, 1)

results = vertical_fdi_separated(
    demand_intercept=a,
    demand_slope=b,
    bearing_cost=c_u,
    machine_cost=c_d,
    bearings_per_machine=k
)

st.subheader('Equilibrium Outcomes')

st.write(f"Ball Bearing Price: {results['ball_bearing_price']: .2f}")
st.write(f"Ball Bearing Quantity: {results['bearing_quantity']: .2f}")

st.write(f"Machine Price: {results['machine_price']: .2f}")
st.write(f"Machine Quantity: {results['machine_quantity']: .2f}")

st.write(f"Upstream Profit: {results['upstream_profit']: .2f}")
st.write(f"Downstream Profit: {results['downstream_profit']: .2f}")


# --- Interactive Profit vs Pb Plot ---
Pb_vals = np.linspace(0, results['ball_bearing_price']*2, 100)
pi_S_vals, pi_G_vals = [], []

for Pb in Pb_vals:
    Q_temp = max(0, (a - c_d - k*Pb)/(2*b))
    P_temp = max(0, a - b*Q_temp)
    pi_S_vals.append(max(0, (2*Pb - c_u)*Q_temp))
    pi_G_vals.append(max(0, P_temp*Q_temp - c_d*Q_temp - Pb*k*Q_temp))

fig = go.Figure()
fig.add_trace(go.Scatter(x=Pb_vals, y=pi_S_vals, mode='lines', name='Upstream Profit'))
fig.add_trace(go.Scatter(x=Pb_vals, y=pi_G_vals, mode='lines', name='Downstream Profit'))
fig.add_vline(x=results['ball_bearing_price'], line=dict(color='gray', dash='dash'), annotation_text="Equilibrium Pb")

fig.update_layout(title="Profit vs Ball-Bearing Price",
                  xaxis_title="Ball-Bearing Price",
                  yaxis_title="Profit",
                  template="plotly_white")

st.plotly_chart(fig, use_container_width=True)