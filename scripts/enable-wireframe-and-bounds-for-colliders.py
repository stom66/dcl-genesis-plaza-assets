import bpy

for obj in bpy.data.objects:
    if "_collider" in obj.name:
        obj.display_type = "WIRE"
        obj.show_bounds = True
        