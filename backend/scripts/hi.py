import matplotlib.pyplot as plt

# Sample table data (modify as per your dataset)
headers = ["Path", "Start Point", "End Point", "Distance"]
data = [
    ["Path 1", "(x1, y1)", "(x2, y2)", "100m"],
    ["Path 2", "(x3, y3)", "(x4, y4)", "150m"],
    ["Path 3", "(x5, y5)", "(x6, y6)", "200m"]
]

# Create the figure
fig, ax = plt.subplots(figsize=(8, 6))  # ⬅ Increased figure size

ax.set_title("Shortest Paths Information", fontsize=20, fontweight='bold')  # Bigger title
ax.axis("tight")
ax.axis("off")

# Create table with bigger font size
table = ax.table(cellText=data, colLabels=headers, cellLoc="center", loc="center")

# Increase font size for table
table.auto_set_font_size(False)
table.set_fontsize(14)  # ⬅ Bigger text
table.scale(2, 2)  # ⬅ Scale up the whole table (increase width & height)

plt.show()
