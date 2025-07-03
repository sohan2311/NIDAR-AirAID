from pdb import  set_trace as st
import bpy
import os

# --- 1. USER SETTINGS ---
# Path to your KML file defining the area boundary
KML_FILEPATH = "test1kml"
# Path where the final .blend file will be saved
OUTPUT_BLEND_FILEPATH = "test1.blend"

# --- 2. AUTOMATION SCRIPT ---
def generate_environment():
    """
    Main function to generate the 3D environment from a KML file.
    """
    print("--- Starting Environment Generation ---")

    # Clean the default scene (cube, light, camera)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    print("Cleaned the scene.")
    st()
    # Import the KML file to define the area
    # Note: BlenderGIS will automatically frame the view on the import
    print(f"Importing KML from: {KML_FILEPATH}")
    bpy.ops.import_geodata.kml(filepath=KML_FILEPATH)
    print("KML imported.")

    # Get DEM (Elevation Data) for the framed area
    print("Fetching Digital Elevation Model (DEM)...")
    bpy.ops.gis.get_dem(dem_source="SRTM_30")
    print("DEM data applied.")
    st()
    # Select the newly created DEM object to apply imagery
    try:
        dem_object = next(obj for obj in bpy.context.scene.objects if "SRTM" in obj.name)
        bpy.context.view_layer.objects.active = dem_object
        dem_object.select_set(True)
    except StopIteration:
        print("ERROR: Could not find the DEM object. Aborting.")
        return

    # Get Satellite Imagery and drape it on the DEM
    print("Fetching satellite imagery...")
    bpy.ops.gis.get_imagery(map_source="GOOGLE", map_layer="SATELLITE")
    print("Imagery applied.")
    st()
    # Save the final .blend file
    print(f"Saving final scene to: {OUTPUT_BLEND_FILEPATH}")
    bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_BLEND_FILEPATH)

    print("--- Environment Generation Complete! ---")

# --- 3. EXECUTION ---
if __name__ == "__main__":
    generate_environment()