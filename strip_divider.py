import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import box, Point
from shapely.affinity import rotate

class StripDivider:
    def __init__(self, kml_path, water_shp_path, output_kml_path, strip_width=20, angle_deg=0, ground_point=None):
        self.kml_path = kml_path
        self.water_shp_path = water_shp_path
        self.output_kml_path = output_kml_path
        self.strip_width = strip_width
        self.angle_deg = angle_deg
        self.ground_point = ground_point
        self.gdf = None
        self.poly = None
        self.gdf_strips = None
        self.water_layer = None

    def load_polygon(self):
        self.gdf = gpd.read_file(self.kml_path, driver="KML")
        self.gdf = self.gdf.to_crs(epsg=32643)
        poly = self.gdf.geometry.iloc[0]
        if poly.geom_type == 'MultiPolygon':
            poly = list(poly.geoms)[0]
        self.poly = poly

    def divide_polygon_into_strips(self):
        minx, miny, maxx, maxy = self.poly.bounds
        width = maxx - minx
        height = maxy - miny
        diagonal_length = (width**2 + height**2) ** 0.5
        num_strips = int(diagonal_length / self.strip_width) + 2
        strips = []
        for i in range(-num_strips, num_strips):
            y_offset = miny + i * self.strip_width
            line = box(minx - diagonal_length, y_offset, maxx + diagonal_length, y_offset + self.strip_width)
            rotated_line = rotate(line, self.angle_deg, origin='center', use_radians=False)
            intersection = self.poly.intersection(rotated_line)
            if not intersection.is_empty:
                if intersection.geom_type == 'Polygon':
                    strips.append(intersection)
                elif intersection.geom_type == 'MultiPolygon':
                    strips.extend(list(intersection.geoms))
       
        self.gdf_strips = gpd.GeoDataFrame(geometry=strips, crs=self.gdf.crs)

    def load_water_layer(self):
        self.water_layer = gpd.read_file(self.water_shp_path).to_crs(self.gdf.crs)

    def add_flags(self):
        self.gdf_strips["has_water"] = False
        self.gdf_strips["has_building"] = False  # Placeholder for future building logic
        if self.water_layer is not None and not self.water_layer.empty:
            for i, row in self.gdf_strips.iterrows():
                strip = row.geometry
                if strip.intersects(self.water_layer.unary_union):
                    self.gdf_strips.at[i, "has_water"] = True

    def compute_distances(self):
        if self.ground_point is not None:
            self.gdf_strips["distance_to_station"] = self.gdf_strips.geometry.centroid.distance(self.ground_point)
        else:
            self.gdf_strips["distance_to_station"] = 0

    def get_priority(self, row):
        if row["has_water"]:
            return 1
        elif row["has_building"]:
            return 2
        else:
            return 3

    def prioritize_and_number(self):
        self.gdf_strips["priority_group"] = self.gdf_strips.apply(self.get_priority, axis=1)
        self.gdf_strips = self.gdf_strips.sort_values(by=["priority_group", "distance_to_station"], ascending=[True, False])
        self.gdf_strips["strip_order"] = range(1, len(self.gdf_strips)+1)

    def plot_strips(self):
        fig, ax = plt.subplots(figsize=(10, 10))
        x, y = self.poly.exterior.xy
        ax.plot(x, y, color='black')
        ax.fill(x, y, alpha=0.1)
        for i, row in self.gdf_strips.iterrows():
            strip = row.geometry
            x, y = strip.exterior.xy
            ax.fill(x, y, alpha=0.5)
            centroid = strip.centroid
            ax.text(centroid.x, centroid.y, f"{row['strip_order']}", fontsize=8, ha='center', va='center')
        plt.title("Strips with priority logic using GEE water/building data")
        plt.axis('equal')
        plt.show()

    def export_kml(self):
        gdf_strips_wgs84 = self.gdf_strips.to_crs(epsg=4326)
        gdf_strips_wgs84.to_file(self.output_kml_path, driver="KML")
        print(f"KML file saved as '{self.output_kml_path}'")

    def run(self):
        self.load_polygon()
        self.divide_polygon_into_strips()
        self.load_water_layer()
        self.add_flags()
        self.compute_distances()
        self.prioritize_and_number()
        self.plot_strips()
        self.export_kml()

# Example usage:
ground_point = Point(825600, 1744600)
divider = StripDivider(
    kml_path="input_strips/new_area.kml",
    water_shp_path="input_strips/Water_Polygons.shp",
    output_kml_path="output_strips/new_area_Strips.kml",
    strip_width=20,
    angle_deg=0,
    ground_point=ground_point
)
divider.run() 