import ezdxf
import matplotlib.pyplot as plt
from collections import defaultdict

# Load DXF file
doc = ezdxf.readfile(r"V:\Warehouse DFX viewer\uploads\warehouse_layout_with_grid.dxf")
msp = doc.modelspace()

# Setup plot
fig, ax = plt.subplots(figsize=(14, 10))
ax.set_aspect("equal")
ax.set_title("Warehouse Layout with Rack-wise Storage Boxes")

# Colors for visualization
rack_color = 'steelblue'
shelf_color = 'gray'
counter_color = 'lightgreen'
box_color = 'orange'

# Structures to hold detected elements
racks = []  # (xmin, ymin, xmax, ymax, label)
boxes = []  # (xmin, ymin, xmax, ymax)
texts = {}  # (x, y) -> text

# First pass to extract all TEXT elements
for entity in msp:
    if entity.dxftype() == 'TEXT':
        x, y = entity.dxf.insert.x, entity.dxf.insert.y  # Correct way to access x and y
        texts[(round(x, 1), round(y, 1))] = entity.dxf.text

# Second pass to extract racks and boxes
for entity in msp:
    if entity.dxftype() == 'LWPOLYLINE':
        points = [(v[0], v[1]) for v in entity]  # Get points of LWPOLYLINE
        if len(points) < 4:
            continue
        x_vals, y_vals = zip(*points)
        xmin, xmax = min(x_vals), max(x_vals)
        ymin, ymax = min(y_vals), max(y_vals)

        width = round(xmax - xmin, 2)
        height = round(ymax - ymin, 2)

        # Check near bottom-left corner for rack label
        label = texts.get((round(xmin + 0.5, 1), round(ymin + 0.2, 1)), None)

        if label and label.startswith("Rack"):
            # It's a rack boundary
            racks.append((xmin, ymin, xmax, ymax, label))
            ax.plot(x_vals, y_vals, color=rack_color, linewidth=2)
            ax.text(xmin + 0.2, ymax + 0.2, label, fontsize=8, color='navy')
        else:
            # Assume it's a box (grid within racks)
            boxes.append((xmin, ymin, xmax, ymax))
            ax.plot(x_vals, y_vals, color=box_color, linewidth=1, linestyle='--')

    elif entity.dxftype() == 'LINE':
        start = entity.dxf.start
        end = entity.dxf.end
        ax.plot([start[0], end[0]], [start[1], end[1]], color=shelf_color, linewidth=1)

# Associate boxes with racks
rack_boxes = defaultdict(list)

for box in boxes:
    bxmin, bymin, bxmax, bymax = box
    center_x = (bxmin + bxmax) / 2
    center_y = (bymin + bymax) / 2

    for rack in racks:
        xmin, ymin, xmax, ymax, label = rack
        if xmin <= center_x <= xmax and ymin <= center_y <= ymax:
            rack_boxes[label].append((bxmax - bxmin, bymax - bymin))  # (width, height)
            break

# Print rack-wise box info
print("\n--- Rack-wise Storage Box Report ---")
for label, box_list in rack_boxes.items():
    box_count = len(box_list)
    sizes = set(f"{round(w, 2)}x{round(h, 2)}" for w, h in box_list)
    print(f"{label}: {box_count} boxes | Sizes: {', '.join(sizes)}")

# Axis setup
ax.set_xlabel("X (meters)")
ax.set_ylabel("Y (meters)")
ax.grid(True)
plt.tight_layout()
plt.show()