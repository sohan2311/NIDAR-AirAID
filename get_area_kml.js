var roi = geometry;

// Export the drawn polygon as a KML file
Export.table.toDrive({
  collection: ee.FeatureCollection([ee.Feature(roi)]),
  description: 'Export_ROI_KML',
  fileFormat: 'KML'
});
