import bpy


def is_asset(collection):
    return collection.asset_data is not None


def is_collection_visible(collection):
    """Check if collection is enabled in the active view layer"""
    def recurse(layer_col):
        if layer_col.collection == collection:
            return not layer_col.exclude
        for child in layer_col.children:
            result = recurse(child)
            if result is not None:
                return result
        return None

    return recurse(bpy.context.view_layer.layer_collection)


def has_root_parent(collection):
    """Check if objects are already parented to a .root empty"""
    for obj in collection.objects:
        if obj.parent and obj.parent.name.endswith(".root"):
            return True
    return False


def create_root_empty_in_collection(collection):
    name = f"{collection.name}.root"

    if name in bpy.data.objects:
        return bpy.data.objects[name]

    empty = bpy.data.objects.new(name, None)
    empty.empty_display_type = 'PLAIN_AXES'
    empty.location = (0, 0, 0)

    # Link to the correct collection
    collection.objects.link(empty)

    return empty


def parent_objects_to_empty(collection, empty):
    for obj in collection.objects:
        if obj == empty:
            continue

        # Preserve world transform
        obj.parent = empty
        obj.matrix_parent_inverse = empty.matrix_world.inverted()


def process():
    collections = bpy.data.collections

    processed = 0
    skipped = 0

    for col in collections:
        # ✅ Asset check
        if not is_asset(col):
            continue

        # ✅ Visibility check
        if not is_collection_visible(col):
            continue

        # ✅ Already processed check
        if has_root_parent(col):
            print(f"⏭ Skipping '{col.name}' (already has root parent)")
            skipped += 1
            continue

        empty = create_root_empty_in_collection(col)
        parent_objects_to_empty(col, empty)

        print(f"✅ Processed: {col.name}")
        processed += 1

    print(f"\nDone. Processed: {processed}, Skipped: {skipped}")


process()