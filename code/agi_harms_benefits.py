'''
This code generates a humorous xkcd-style plot illustrating the concept of "EXPO-HARM" in AI development, where harmful AI technologies grow exponentially while beneficial AI technologies grow more slowly due to institutional constraints. The plot emphasizes the "velocity gap" between the two trajectories, highlighting the potential risks of unregulated AI growth compared to the slower pace of beneficial advancements.
'''

import matplotlib.pyplot as plt
import numpy as np

# Enable xkcd style (hand-drawn look)
plt.xkcd()

# Generate sample data points
# x represents time
x = np.linspace(0, 10, 100)

# Harmful AI Technologies: Exponential growth (speed of code)
y_harm = 0.1 * np.exp(0.45 * x) 

# Beneficial AI Technologies: Logarithmic/Sigmoid style growth (human institutional speed)
# This represents a curve that starts strong but plateaus due to bureaucracy and consensus
y_benefit = 2.5 * (1 - np.exp(-0.4 * x)) + 0.5

# Create the visualization
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the two trajectories
ax.plot(x, y_harm, color='red', linewidth=3, label='Harmful AI Technologies')
ax.plot(x, y_benefit, color='tab:blue', linewidth=3, label='Beneficial AI Technologies')

# Add titles and labels
ax.set_xlabel('Time', fontsize=14)
ax.set_ylabel('Progress & Impact', fontsize=14)
ax.set_title('AI Trajectories: Harm vs. Benefit', fontsize=18, pad=20)

# Remove standard tick marks to emphasize the conceptual nature
ax.set_xticks([])
ax.set_yticks([])

# Add annotations to explain the 'Velocity Gap'
ax.annotate('Institutional Constraints\n& Policy Bottlenecks', 
            xy=(5, 2.8), xytext=(4, 4),
            arrowprops=dict(arrowstyle='->', color='black'))

ax.annotate('Unregulated Growth', 
            xy=(8, 4), xytext=(5, 6),
            arrowprops=dict(arrowstyle='->', color='red'))

# Adding descriptive text to the plot
ax.text(9, 8, 'EXPO-HARM!', color='red', fontsize=12, fontweight='bold')
ax.text(9, 3.2, 'The "Human"\nPlateau', color='tab:blue', fontsize=12)

# Place the legend
ax.legend(loc='upper left')

# Adjust layout and save the result
plt.tight_layout()
plt.savefig('ai_xkcd_plot.png')
print("Plot generated and saved as 'ai_xkcd_plot.png'")