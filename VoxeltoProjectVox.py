import json
import uuid
from voxypy.models import Entity
import tkinter as tk
from tkinter import filedialog

# File choose dialog
file_path = filedialog.askopenfilename(
    title="Select a File To Convert",
    filetypes=[("Vox files", "*.vox")]
)
entity = Entity().from_file(file_path)

dimensions = entity.get_dense().shape
Colors = entity.get_dense()




iterate = 0

# Im not sure if i need to change this for every run
project_id = "b6e482c848b8831c43ebb75e345013d6"

# List of Parts of json use
parts_list = []

# Function to Make Parts
def add_part(name, x, y, z, r, g, b, a):
    part = {
        "name": name,
        "position": {"x": x, "y": y, "z": z},
        "rotation": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
        "color": {"r": r, "g": g, "b": b, "a": a},
        "material": "Plastic",
        "group": None,
        "cast_shadow": True,
        "anchored": True,
        "can_collide": True,
        "spawn_location": False,
        "baseplate": False,
        "custom_appearance": False,
        "truss": False,
        "textures": []
    }
    parts_list.append(part)

xd, yd, zd = dimensions
# Loops Through the Entity size
for x in range(xd):
  for y in range(yd):
     for z in range(zd):
      voxel = entity.get(x, y, z)
      color_index = voxel.get()
      if color_index != 0: # if there is a voxel
        palette = entity.get_palette(padded=True)
        r, g, b, a = palette[color_index]
        add_part(f"Part{iterate}", x, z, y, r/255.0, g/255.0, b/255.0, a/255.0)
        iterate += 1 # This is For naming the parts

# Data that gets Converted into josn
final_data = {
    "project_id": project_id,
    "parts": parts_list  
    ,
  "lights": [
    {
      "name": "Light",
      "position": {
        "x": 50.0,
        "y": 80.0,
        "z": 30.0
      },
      "rotation": {
        "x": -0.39447272,
        "y": 0.43916786,
        "z": 0.22334667,
        "w": 0.775654
      },
      "color": {
        "r": 0.99999994,
        "g": 0.99999994,
        "b": 0.99999994,
        "a": 1.0
      },
      "illuminance": 10000.0,
      "shadows_enabled": True
    }
  ],
  "groups": []
}

# Output path for file
output_path = filedialog.asksaveasfilename(
        title="Save Output File",
        defaultextension=".json",
        filetypes=[("Output file", "*.json")],
        initialfile="Converter_Output.josn"
    )
# Writing the josn
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(final_data, f, indent=2)

print(f"Successfully wrote {len(parts_list)} parts to {output_path}.")   
