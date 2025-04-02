import matplotlib.pyplot as plt

# Example data
lap_numbers = [1, 2, 3, 4, 5]
speeds1 = [120, 110, 130, 115, 125]
speeds2 = [100, 90, 110, 105, 115]
drivers = ['Driver 1', 'Driver 2']

# Create the figure and axes
fig, axes = plt.subplots(len(drivers), 1, figsize=(10, 6))

# Plot each driver's data in a separate plot
for i, driver in enumerate(drivers):
    axes[i].bar(lap_numbers, speeds1, width=0.4, color='blue', label='Speed 1')
    axes[i].bar([x + 0.4 for x in lap_numbers], speeds2, width=0.4, color='green', label='Speed 2')

    axes[i].set_xlabel('Lap Number')
    axes[i].set_ylabel('Speed (km/h)')
    axes[i].set_title(f'{driver} Speed vs Lap Number')
    axes[i].legend()

plt.tight_layout()
plt.show()
