import bpy

def sort_child_collections(parent_collection):
    # Get child collections
    children = list(parent_collection.children)

    # Sort them alphabetically by name
    children_sorted = sorted(children, key=lambda c: c.name.lower())

    # Unlink all children first
    for child in children:
        parent_collection.children.unlink(child)

    # Re-link in sorted order
    for child in children_sorted:
        parent_collection.children.link(child)

    print(f"Sorted {len(children_sorted)} collections in '{parent_collection.name}'")


# Run on active collection
context = bpy.context
layer_collection = context.view_layer.active_layer_collection
collection = layer_collection.collection

sort_child_collections(collection)