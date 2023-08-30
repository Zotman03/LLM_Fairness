import matplotlib.pyplot as plt

# Create a figure with 3 subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(10, 12))

# Hide the axes
ax1.axis('off')
ax2.axis('off')
ax3.axis('off')

# Data for the tables
data1 = [["", "Respondent Type", "", "", "Direction", ""], [r"$\uparrow \overline{mF1}$", "GD", r"$\uparrow mF1_W$", r"$\uparrow \overline{mF1}$", "GD", r"$\uparrow mF1_W$"], ["0.22577", "0.00000005949", "0.14444", "0.2641", "0.00014652", "0.24971"], ["Group", "mF1", "Accuracy", "Group", "mF1", "Accuracy"], ["Person", "0.26784", "43.3%", "Conservative", "0.24971", "36.4%"], ["Organization", "0.19638", "25.2%", "Liberal", "0.27849", "33.9%"], ["Public entity", "0.31011", "39.7%", "", "", ""], ["Facility", "0.14444", "16.1%", "", "", ""], ["Other", "0.21009", "18.1%", "", "", ""]]
data2 = [["", "Language", "", "", "Legal Area", "", "", "Region", ""], [r"$\uparrow \overline{mF1}$", "GD", r"$\uparrow mF1_W$", r"$\uparrow \overline{mF1}$", "GD", r"$\uparrow mF1_W$", r"$\uparrow \overline{mF1}$", "GD", r"$\uparrow mF1_W$"], ["0.42829", "0.00019221", "0.29851", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]]
data3 = [["", "Defendant Gender", "", "", "Region", ""], [r"$\uparrow \overline{mF1}$", "GD", r"$\uparrow mF1_W$", r"$\uparrow \overline{mF1}$", "GD", r"$\uparrow mF1_W$"], ["0.12149", "0.000062669", "0.11207", "0.15092", "0.000000000021261", "0.07533"], ["Group", "mF1", "Accuracy", "Group", "mF1", "Accuracy"], ["Male", "0.11207", "25%", "Beijing", "0.18693", "23.7%"], ["Female", "0.13090", "19.5%", "Liaoning", "0.10427", "17.2%"], ["", "", "", "Hunan", "0.07533", "6.3%"], ["", "", "", "Guangdong", "0.20428", "32.6%"], ["", "", "", "Sichuan", "0.1346", "21.9%"], ["", "", "", "Guangxi", "0.16572", "25.4%"], ["", "", "", "Zhejiang", "0.18528", "34.2%"]]

# Create the tables
table1 = ax1.table(cellText=data1, loc='center')
table2 = ax2.table(cellText=data2, loc='center')
table3 = ax3.table(cellText=data3, loc='center')

# Make the cells larger to fit the text
for table in [table1, table2, table3]:
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.5, 1.5)

# Add titles
ax1.set_title("SCOTUS")
ax2.set_title("FSCS")
ax3.set_title("CAIL")

# Show the plot
plt.tight_layout()
plt.show()
