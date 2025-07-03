# # # No longer importing pdb
# .\blender.exe --background --python "C:\Users\DHRUV SINGH\Desktop\drone_simulation\blender_run1.py" "C:\Users\DHRUV SINGH\Desktop\drone_simulation\airaid" 

# import bpy
# import os
# from pdb import set_trace as st
# # --- 1. USER SETTINGS ---
# # Use absolute paths to avoid errors in headless mode.
# # os.path.abspath() converts a relative path to an absolute one.
# # Replace "." with the actual directory containing your files.
# if not bpy.context.preferences.addons.get("BlenderGIS-master"):
#     bpy.ops.preferences.addon_enable(module="BlenderGIS-master")
# st()    
# script_directory = os.path.dirname(os.path.realpath(__file__))
# KML_FILEPATH = os.path.join(script_directory, "test1.kml") # Make sure file has .kml extension
# OUTPUT_BLEND_FILEPATH = os.path.join(script_directory, "test1.blend")

# # --- 2. AUTOMATION SCRIPT ---
# def generate_environment():
#     """
#     Main function to generate the 3D environment from a KML file.
#     """
#     print("--- Starting Environment Generation ---")

#     # Clean the default scene (cube, light, camera)
#     bpy.ops.object.select_all(action='SELECT')
#     bpy.ops.object.delete()
#     print("Cleaned the scene.")
    
#     # --- FIX 1: Create a context override ---
#     # GIS operators need a 3D View context to run in scripts.
#     # We define it once and reuse it for all operator calls.
#     win = bpy.context.window
#     scr = win.screen
#     area_3d = next((area for area in scr.areas if area.type == 'VIEW_3D'), None)
#     if area_3d is None:
#         print("ERROR: No 3D Viewport found. Cannot run GIS operators.")
#         return
        
#     region_3d = next(region for region in area_3d.regions if region.type == 'WINDOW')

#     override = {
#         'window': win,
#         'screen': scr,
#         'area': area_3d,
#         'region': region_3d,
#         'scene': bpy.context.scene,
#     }

#     # Import the KML file using the context override
#     print(f"Importing KML from: {KML_FILEPATH}")
#     if not os.path.exists(KML_FILEPATH):
#         print(f"ERROR: KML file not found at '{KML_FILEPATH}'. Aborting.")
#         return
#     # --- FIX 2: Apply the override to the operator ---
#     bpy.ops.import_geodata.kml( filepath=KML_FILEPATH)
#     print("KML imported.")
#     st()
#     # Get DEM (Elevation Data) using the context override
#     print("Fetching Digital Elevation Model (DEM)...")
#     bpy.ops.gis.get_dem(override, dem_source="SRTM_30")
#     print("DEM data applied.")

#     # Select the newly created DEM object to apply imagery
#     try:
#         dem_object = next(obj for obj in bpy.context.scene.objects if "SRTM" in obj.name)
#         bpy.context.view_layer.objects.active = dem_object
#         dem_object.select_set(True)
#     except StopIteration:
#         print("ERROR: Could not find the DEM object. Aborting.")
#         return

#     # Get Satellite Imagery using the context override
#     print("Fetching satellite imagery...")
#     bpy.ops.gis.get_imagery(override, map_source="GOOGLE", map_layer="SATELLITE")
#     print("Imagery applied.")
    
#     # Save the final .blend file
#     print(f"Saving final scene to: {OUTPUT_BLEND_FILEPATH}")
#     bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_BLEND_FILEPATH)

#     print("--- Environment Generation Complete! ---")

# # --- 3. EXECUTION ---
# if __name__ == "__main__":
#     generate_environment()
import bpy
import os
import bmesh
from pykml import parser

# --- 1. USER SETTINGS ---
script_directory = os.path.dirname(os.path.realpath(__file__))
KML_FILEPATH = os.path.join(script_directory, "test1.kml")
OUTPUT_BLEND_FILEPATH = os.path.join(script_directory, "test1.blend")


# --- 2. Helper function: Create polygon mesh ---
def create_polygon(coords, name="PolygonObj"):
    mesh = bpy.data.meshes.new(name + "_Mesh")
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()
    verts = [bm.verts.new((x, y, z)) for x, y, z in coords]

    if len(verts) >= 3:
        try:
            bm.faces.new(verts)
        except:
            print("Warning: Could not create face (possible non-manifold or duplicate verts)")

    bm.to_mesh(mesh)
    bm.free()


# --- 3. Parse KML file and extract polygons ---
def import_kml_polygons(kml_path):
    with open(kml_path) as f:
        doc = parser.parse(f).getroot()

    # Try to access Placemarks
    try:
        placemarks = doc.Document.Folder.Placemark
    except AttributeError:
        placemarks = doc.Document.Placemark

    for i, pm in enumerate(placemarks):
        if hasattr(pm, 'Polygon'):
            coords_text = pm.Polygon.outerBoundaryIs.LinearRing.coordinates.text.strip()
            coords = []
            for line in coords_text.split():
                lon, lat, alt = map(float, line.split(','))
                # Simple scaling so that coordinates are in Blender scene range
                coords.append((lon * 100, lat * 100, alt))
            
            create_polygon(coords, name=f"PolygonObj_{i}")

        elif hasattr(pm, 'Point'):
            coords_text = pm.Point.coordinates.text.strip()
            lon, lat, alt = map(float, coords_text.split(','))
            # Create small cube as marker
            bpy.ops.mesh.primitive_cube_add(size=10, location=(lon * 100, lat * 100, alt))
            obj = bpy.context.active_object
            obj.name = f"PointObj_{i}"

        elif hasattr(pm, 'LineString'):
            coords_text = pm.LineString.coordinates.text.strip()
            coords = []
            for line in coords_text.split():
                lon, lat, alt = map(float, line.split(','))
                coords.append((lon * 100, lat * 100, alt))
            
            # Create a simple polyline as mesh
            mesh = bpy.data.meshes.new(f"LineObj_{i}_Mesh")
            obj = bpy.data.objects.new(f"LineObj_{i}", mesh)
            bpy.context.collection.objects.link(obj)

            bm = bmesh.new()
            verts = [bm.verts.new((x, y, z)) for x, y, z in coords]

            for v1, v2 in zip(verts[:-1], verts[1:]):
                bm.edges.new([v1, v2])

            bm.to_mesh(mesh)
            bm.free()


# --- 4. Main function ---
def generate_environment():
    print("--- Starting Environment Generation ---")

    # Clean the default scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    print("Cleaned the scene.")

    # Check KML file
    print(f"Importing KML from: {KML_FILEPATH}")
    if not os.path.exists(KML_FILEPATH):
        print(f"ERROR: KML file not found at '{KML_FILEPATH}'. Aborting.")
        return

    # Parse and create geometry
    import_kml_polygons(KML_FILEPATH)
    print("KML geometry created.")

    # Save the final .blend file
    print(f"Saving final scene to: {OUTPUT_BLEND_FILEPATH}")
    bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_BLEND_FILEPATH)

    print("--- Environment Generation Complete! ---")


# --- 5. EXECUTION ---
if __name__ == "__main__":
    generate_environment()
