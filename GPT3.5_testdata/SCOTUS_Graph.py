import matplotlib.pyplot as plt

# Create a figure and axes (3 rows, 1 column)
fig, axs = plt.subplots(3, 1, figsize=(10, 6))

# Hide the axes for all subplots
for ax in axs:
    ax.axis('off')

# Create the first table
data = [
    ["Group", "mF1", "Accuracy"],
    ["Liberal", "0.27849", "33.9%"],
    ["Conservative", "0.24971", "36.4%"]
]

table = axs[0].table(cellText=data,
                     loc='center',
                     colWidths=[0.2] * 3)
table.auto_set_font_size(False)
table.set_fontsize(8)

# Create the second table
data1 = [
    ["Group", "mF1", "Accuracy"],
    ["Person", "0.26784", "43.3%"],
    ["Organization", "0.19638", "25.2%"],
    ["Public entity", "0.31011", "39.7%"],
    ["Facility", "0.14444", "16.1%"],
    ["Other", "0.21009", "18.1%"]
]

table1 = axs[1].table(cellText=data1,
                      loc='center',
                      colWidths=[0.2] * 3)
table1.auto_set_font_size(False)
table1.set_fontsize(8)

# Create the third table
data2 = [
    ["Group", "Accuracy"],
    ["Total Accuracy", "35.1%"]
]

table2 = axs[2].table(cellText=data2,
                      loc='center',
                      colWidths=[0.2] * 2)
table2.auto_set_font_size(False)
table2.set_fontsize(8)

# Add title
plt.suptitle("SCOTUS")

# Ensure the subplots do not overlap
plt.subplots_adjust(hspace=0.2)

# Show the plot
plt.show()
