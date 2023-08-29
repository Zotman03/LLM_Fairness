import matplotlib.pyplot as plt

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 4))

# Hide the axes
ax.axis('off')

# Create the table
data = [
    ["Group", r"$\uparrow \overline{mF1}$", "GD", r"$\uparrow mF1_W$"],
    ["Respondent type", "0.22577", "0.00000005949", "0.14444"],
    ["Direction", "0.2641", "0.00014652", "0.24971"]
]

table = ax.table(cellText=data,
                 loc='center',
                 colWidths=[0.2] * 4)

# Make the cells larger to fit the text
table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width(col=list(range(4)))

# Add title closer to the table
plt.title("SCOTUS", y=0.6)  # Adjust y to move the title up or down

# Show the plot
plt.show()
