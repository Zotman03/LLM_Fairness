import matplotlib.pyplot as plt

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 4))

# Hide the axes
ax.axis('off')

# Create the table
data = [
    ["Group", r"$\uparrow \overline{mF1}$", "GD", r"$\uparrow mF1$"],
    ["Defender Gender", "0.12149", "0.000062669", "0.11207"],
    ["Region", "0.15092", "0.000000000021261", "0.07533"]
]

table = ax.table(cellText=data,
                 loc='center',
                 colWidths=[0.2] * 4)

# Make the cells larger to fit the text
table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width(col=list(range(4)))

# Add title closer to the table
plt.title("CAIL", y=0.6)  # Adjust y to move the title up or down

# Show the plot
plt.show()
