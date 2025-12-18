import streamlit as st
import numpy as np
import plotly.graph_objects as go
from model import vertical_fdi_separated, vertical_fdi_integrated

st.title('Vertical FDI Simulation')

# --- Sliders ---
a = st.slider("Demand Intercept (a)", 100, 2000, 240)
b = st.slider("Demand Slope (b)", 1, 10, 2, 1)
c_u = st.slider("Upstream Cost (Ball Bearings)", 0, 150, 6, 1)
c_d = st.slider("Downstream Cost (Machines)", 0, 150, 4, 1)
k = st.slider("Bearings per Machine", 1, 20, 2, 1)
fc = st.slider("Fixed Cost (MNC)", 0, 5000, 1000, 100)

# --- Compute Results ---
sep_results = vertical_fdi_separated(a, b, c_u, c_d, k)
int_results = vertical_fdi_integrated(a, b, c_u, c_d, k, fc)


# --- Separated Firms Column ---
st.subheader("Separated Firms")

# Profit vs Pb Graph
max_x = 200
max_y = 7000
Pb_vals = np.linspace(0, max_x, 300)
pi_S_vals, pi_G_vals = [], []
for Pb in Pb_vals:
    Q_temp = max(0, (a - c_d - k*Pb)/(2*b))
    P_temp = max(0, a - b*Q_temp)
    pi_S_vals.append(max(0, (2*Pb - c_u)*Q_temp))
    pi_G_vals.append(max(0, (P_temp * Q_temp - c_d * Q_temp - Pb * k * Q_temp)))

fig_sep = go.Figure()
fig_sep.add_trace(go.Scatter(x=Pb_vals, y=pi_S_vals, mode='lines', name='Upstream Profit'))
fig_sep.add_trace(go.Scatter(x=Pb_vals, y=pi_G_vals, mode='lines', name='Downstream Profit'))
fig_sep.add_vline(x=sep_results['ball_bearing_price'], line=dict(color='white', dash='dot'), annotation_text="Equilibrium Pb")
fig_sep.add_trace(go.Scatter(
    x=[sep_results['ball_bearing_price']], 
    y=[sep_results['upstream_profit']], 
    mode='markers', 
    marker=dict(color='blue', size=10), 
    name='Upstream Equilibrium'
))
fig_sep.add_trace(go.Scatter(
    x=[sep_results['ball_bearing_price']], 
    y=[sep_results['downstream_profit']], 
    mode='markers', 
    marker=dict(color='green', size=10), 
    name='Downstream Equilibrium'
))
fig_sep.update_layout(title="Profit vs Pb (Separated Firms)",
                        xaxis_title="Ball Bearing Price",
                        yaxis_title="Profit",
                        xaxis=dict(range=[0, max_x]),
                        yaxis=dict(range=[0, max_y]),
                        height=500)
st.plotly_chart(fig_sep, use_container_width=True)

# Display Equilibrium Outcomes
st.write(sep_results)

# Display dynamic profit functions
st.markdown("**Separated Profit Function:**")
st.latex(r"\pi_S(Q) = (2 P_b - %d) Q" % c_u)
st.latex(r"\pi_G(Q) = ( (a - b Q) Q - %d Q - P_b %d Q )" % (c_d, k))
st.latex(r"\text{Where } P(Q) = %d Q - %d Q" % (a, b))
# --- Integrated Firm Column ---
st.subheader("Integrated Firm")

# Profit vs Pb Graph
pi_I_vals = []
for Pb in Pb_vals:
    Q_temp = max(0, (a - c_d - k*Pb)/(2*b))
    q_temp = k * Q_temp
    P_temp = max(0, a - b*Q_temp)
    pi_I = (P_temp * Q_temp - c_d * Q_temp - Pb*q_temp) + (Pb*q_temp - c_u*q_temp) - fc
    pi_I_vals.append(max(0, pi_I))

fig_int = go.Figure()
fig_int.add_trace(go.Scatter(x=Pb_vals, y=pi_I_vals, mode='lines', name='Integrated Profit', line=dict(color='red', dash='dash')))
fig_int.add_vline(x=int_results['ball_bearing_price'], line=dict(color='white', dash='dot'), annotation_text="Equilibrium Pb")
fig_int.update_layout(title="Profit vs Pb (Integrated Firm)",
                        xaxis_title="Ball Bearing Price",
                        yaxis_title="Profit",
                        xaxis=dict(range=[0, max_x]),
                        yaxis=dict(range=[0, max_y]),
                        height=500)
st.plotly_chart(fig_int, use_container_width=True)

# Display Equilibrium Outcomes
st.write(int_results)

# Display dynamic profit function
st.markdown("**Integrated Profit Function:**")
st.latex(r"\pi_{MNC} = \pi_G + \pi_S - %d" % fc)
st.latex(r"\text{Where } P(Q) = %d - %d Q" % (a, b))
st.latex(r"\pi_S = (P_b * %d Q - %d * %d Q)" % (k, c_u, k))
st.latex(r"\pi_G = ((%d - %d Q) Q - %d Q - P_b * %d Q)" % (a, b, c_d, k))
