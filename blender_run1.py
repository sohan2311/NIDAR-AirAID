# No longer importing pdb
import bpy
import os

# --- 1. USER SETTINGS ---
# Use absolute paths to avoid errors in headless mode.
# os.path.abspath() converts a relative path to an absolute one.
# Replace "." with the actual directory containing your files.
script_directory = os.path.dirname(os.path.realpath(__file__))
KML_FILEPATH = os.path.join(script_directory, "test1.kml") # Make sure file has .kml extension
OUTPUT_BLEND_FILEPATH = os.path.join(script_directory, "test1.blend")

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

    # --- FIX 1: Create a context override ---
    # GIS operators need a 3D View context to run in scripts.
    # We define it once and reuse it for all operator calls.
    win = bpy.context.window
    scr = win.screen
    area_3d = next((area for area in scr.areas if area.type == 'VIEW_3D'), None)
    if area_3d is None:
        print("ERROR: No 3D Viewport found. Cannot run GIS operators.")
        return
        
    region_3d = next(region for region in area_3d.regions if region.type == 'WINDOW')

    override = {
        'window': win,
        'screen': scr,
        'area': area_3d,
        'region': region_3d,
        'scene': bpy.context.scene,
    }

    # Import the KML file using the context override
    print(f"Importing KML from: {KML_FILEPATH}")
    if not os.path.exists(KML_FILEPATH):
        print(f"ERROR: KML file not found at '{KML_FILEPATH}'. Aborting.")
        return
    # --- FIX 2: Apply the override to the operator ---
    bpy.ops.import_geodata.kml(override, filepath=KML_FILEPATH)
    print("KML imported.")

    # Get DEM (Elevation Data) using the context override
    print("Fetching Digital Elevation Model (DEM)...")
    bpy.ops.gis.get_dem(override, dem_source="SRTM_30")
    print("DEM data applied.")

    # Select the newly created DEM object to apply imagery
    try:
        dem_object = next(obj for obj in bpy.context.scene.objects if "SRTM" in obj.name)
        bpy.context.view_layer.objects.active = dem_object
        dem_object.select_set(True)
    except StopIteration:
        print("ERROR: Could not find the DEM object. Aborting.")
        return

    # Get Satellite Imagery using the context override
    print("Fetching satellite imagery...")
    bpy.ops.gis.get_imagery(override, map_source="GOOGLE", map_layer="SATELLITE")
    print("Imagery applied.")
    
    # Save the final .blend file
    print(f"Saving final scene to: {OUTPUT_BLEND_FILEPATH}")
    bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_BLEND_FILEPATH)

    print("--- Environment Generation Complete! ---")

# --- 3. EXECUTION ---
if __name__ == "__main__":
    generate_environment()
