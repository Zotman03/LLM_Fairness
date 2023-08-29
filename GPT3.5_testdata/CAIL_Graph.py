import matplotlib.pyplot as plt

# Create a figure and axes (3 rows, 1 column)
fig, axs = plt.subplots(3, 1, figsize=(10, 6))

# Hide the axes for all subplots
for ax in axs:
    ax.axis('off')

# Create the first table
data = [
    ["Group", "mF1", "Accuracy"],
    ["Male", "0.11207", "25%"],
    ["Female", "0.13090", "19.5%"]
]

table = axs[0].table(cellText=data,
                     loc='center',
                     colWidths=[0.2] * 3)
table.auto_set_font_size(False)
table.set_fontsize(8)

# Create the second table
data1 = [
    ["Group", "mF1", "Accuracy"],
    ["Beijing", "0.18693", "23.7%"],
    ["Liaoning", "0.10427", "17.2%"],
    ["Hunan", "0.07533", "6.3%"],
    ["Guangdong", "0.20428", "32.6%"],
    ["Sichuan", "0.1346", "21.9%"],
    ["Guangxi", "0.16572", "25.4%"],
    ["Zhejiang", "0.18528", "34.2%"]
]

table1 = axs[1].table(cellText=data1,
                      loc='center',
                      colWidths=[0.2] * 3)
table1.auto_set_font_size(False)
table1.set_fontsize(8)

# Create the third table
data2 = [
    ["Group", "Accuracy"],
    ["Total Accuracy", "24.6%"]
]

table2 = axs[2].table(cellText=data2,
                      loc='center',
                      colWidths=[0.2] * 2)
table2.auto_set_font_size(False)
table2.set_fontsize(8)

# Add title
plt.suptitle("CAIL")

# Ensure the subplots do not overlap
plt.subplots_adjust(hspace=0.2)

# Show the plot
plt.show()
