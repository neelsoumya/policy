# AI Velocity Gap Simulator
# This code creates an interactive simulation to visualize the "Velocity Gap" between harmful AI technologies and

# use this if notebook: %matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interact, widgets

def plot_velocity_gap(harm_growth, benefit_ceiling, inst_speed, policy_lag):
    time = np.linspace(0, 25, 250)
    
    # Models
    y_harm = 0.5 * np.exp(harm_growth * time)
    midpoint = 10 + policy_lag
    y_benefit = benefit_ceiling / (1 + np.exp(-inst_speed * (time - midpoint)))
    
    # Calculate Risk Score (Area between curves)
    risk_score = np.trapz(np.maximum(0, y_harm - y_benefit), time)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(time, y_harm, color='red', lw=2, label='Harmful AI Potential')
    plt.plot(time, y_benefit, color='blue', lw=2, label='Realized AI Benefits')
    
    # Fill the gap
    plt.fill_between(time, y_benefit, y_harm, where=(y_harm > y_benefit), 
                     color='red', alpha=0.1, label='The Velocity Gap')
    
    # Formatting
    plt.title(f"AI Velocity Gap | Cumulative Risk: {risk_score:.2f}", fontsize=14)
    plt.xlabel("Years from AGI Emergence")
    plt.ylabel("Impact Magnitude")
    plt.ylim(0, min(max(y_harm)*1.1, 300))
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    
    plt.show()

# Interactive Sliders
interact(
    plot_velocity_gap,
    harm_growth = widgets.FloatSlider(value=0.25, min=0.1, max=0.4, step=0.01),
    benefit_ceiling = widgets.IntSlider(value=50, min=10, max=100, step=5),
    inst_speed = widgets.FloatSlider(value=0.4, min=0.1, max=1.0, step=0.05),
    policy_lag = widgets.IntSlider(value=0, min=-5, max=10, step=1)
);


####################
# legacy code
# The above code is a more interactive and dynamic version of the original static plot. It allows users to adjust parameters and see how they affect the "Velocity Gap" between harmful AI technologies and beneficial AI technologies in real-time. The risk score is calculated as the area between the two curves where harm exceeds benefit, providing a quantitative measure of the potential risk over time.
####################

import numpy as np
import plotly.graph_objects as go
from ipywidgets import interact, widgets

# Ensure the renderer is set for the environment (especially helpful for Colab/VS Code)
import plotly.io as pio
pio.renderers.default = 'colab' # Change to 'notebook' if using classic Jupyter

def simulate_ai_future(harm_growth, benefit_ceiling, inst_speed, policy_lag):
    time = np.linspace(0, 25, 250)
    
    # 1. Exponential Harm Model
    y_harm = 0.5 * np.exp(harm_growth * time)
    
    # 2. Logistic Benefit Model (The 'Institutional' curve)
    # We add the policy_lag to the midpoint of the S-curve
    midpoint = 10 + policy_lag
    y_benefit = benefit_ceiling / (1 + np.exp(-inst_speed * (time - midpoint)))
    
    # 3. Calculate the "Velocity Gap" (Area between curves)
    # We only care about the area where Harm > Benefit
    gap_delta = np.maximum(0, y_harm - y_benefit)
    risk_score = np.trapz(gap_delta, time) # Numerical integration
    
    # 4. Create the Figure
    fig = go.Figure()

    # Harm Trace
    fig.add_trace(go.Scatter(
        x=time, y=y_harm, name='Harmful AI Potential',
        line=dict(color='#ef4444', width=3)
    ))

    # Benefit Trace
    fig.add_trace(go.Scatter(
        x=time, y=y_benefit, name='Realized AI Benefits',
        line=dict(color='#3b82f6', width=3),
        fill='tonexty', fillcolor='rgba(239, 68, 68, 0.1)'
    ))

    # Formatting
    fig.update_layout(
        title=f"<b>AI Velocity Gap Simulator</b><br>Cumulative Risk Score: {risk_score:.2f}",
        xaxis_title="Years from AGI Emergence",
        yaxis_title="Impact Magnitude",
        template="plotly_white",
        yaxis=dict(range=[0, min(max(y_harm)*1.1, 500)]), # Dynamic scaling
        annotations=[
            dict(x=20, y=max(y_harm)*0.8, text=f"Risk Area: {risk_score:.0f} units", showarrow=False)
        ]
    )
    
    fig.show()

# Create the interactive sliders
interact(
    simulate_ai_future,
    harm_growth = widgets.FloatSlider(value=0.25, min=0.1, max=0.4, step=0.01, description='Harm Growth:'),
    benefit_ceiling = widgets.IntSlider(value=50, min=10, max=100, step=5, description='Inst. Capacity:'),
    inst_speed = widgets.FloatSlider(value=0.4, min=0.1, max=1.0, step=0.05, description='Consensus Speed:'),
    policy_lag = widgets.IntSlider(value=0, min=-5, max=10, step=1, description='Policy Lag:')
);