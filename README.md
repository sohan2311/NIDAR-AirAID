# Strip Divider

This system divides a polygon area (from a KML file) into strips, prioritizes them based on the presence of water bodies (from a SHP file), and exports the result as a KML file.

## Requirements

- Python 3.8+
- geopandas
- matplotlib
- shapely

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your input files in the `strips/` folder:
   - `Export_ROI_KML.kml` (area polygon)
   - `Water_Polygons.shp` (water bodies)

2. Edit and run the following example in a Python script or interactive shell:

```python
from shapely.geometry import Point
from strip_divider import StripDivider

ground_point = Point(825600, 1744600)
divider = StripDivider(
    kml_path="input_strips/Export_ROI_KML.kml",
    water_shp_path="input_strips/Water_Polygons.shp",
    output_kml_path="output_strips/Prioritized_Strips.kml",
    strip_width=20,
    angle_deg=0,
    ground_point=ground_point
)
divider.run()
```

The output KML will be saved as `strips/Prioritized_Strips.kml`. 