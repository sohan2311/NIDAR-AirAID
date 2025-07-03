//Run this script in Earth Engine with the geometry of the AOI as the input

// Your drawn polygon or imported polygon as FeatureCollection
 
// Get the geometry
var aoi_geom = geometry
// Global Surface Water dataset
var water = ee.Image("JRC/GSW1_4/GlobalSurfaceWater").select("occurrence");

// Mask water where occurrence > 50% (can change threshold if needed)
var waterMask = water.gt(50);

// Vectorize water mask within AOI
var waterVector = waterMask.selfMask().reduceToVectors({
  geometry: aoi_geom,
  scale: 30,
  geometryType: 'polygon',
  eightConnected: false,
  labelProperty: 'water',
  bestEffort: true,
});

// Export to Drive
Export.table.toDrive({
  collection: waterVector,
  description: 'Water_Polygons',
  fileFormat: 'SHP'
});
