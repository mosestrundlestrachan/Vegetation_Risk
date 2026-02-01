# Process Log - Vegetation Risk Model

## 01_load_and_check.py
**Run time:** 2026-02-01 19:31:28

### Summary

| Layer | Rows | CRS | Issues |
|-------|------|-----|--------|
| tree_canopy | 408,646 | PROJCS["NAD83(2011) / Washingt | Invalid geometries: 4334 |
| city_light_lines | 147,538 | PROJCS["NAD83(HARN) / Washingt | None |
| city_light_poles | 101,269 | PROJCS["NAD83(HARN) / Washingt | None |
| fire_stations | 36 | PROJCS["NAD83(HARN) / Washingt | None |
| hospitals | 19 | PROJCS["NAD83(HARN) / Washingt | None |
| neighborhoods | 94 | EPSG:2926 | None |

### Details

#### tree_canopy
- **Path:** `/Users/moses/Desktop/VegetationRisk_SCL/data/raw/TreeCanopy_Seattle_2021_-5593313463288605630/TreeCanopy_2021_Seattle.shp`
- **Rows:** 408,646
- **CRS:** PROJCS["NAD83(2011) / Washington North (ftUS)",GEOGCS["NAD83(2011)",DATUM["NAD83_National_Spatial_Reference_System_2011",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],AUTHORITY["EPSG","1116"]],PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433]],PROJECTION["Lambert_Conformal_Conic_2SP"],PARAMETER["latitude_of_origin",47],PARAMETER["central_meridian",-120.833333333333],PARAMETER["standard_parallel_1",47.5],PARAMETER["standard_parallel_2",48.7333333333333],PARAMETER["false_easting",1640416.66666667],PARAMETER["false_northing",0],UNIT["US survey foot",0.304800609601219,AUTHORITY["EPSG","9003"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]
- **Geometry:** ['Polygon']
- **Columns:** ['Id', 'gridcode', 'geometry']
- **Issues:** Invalid geometries: 4334

#### city_light_lines
- **Path:** `/Users/moses/Desktop/VegetationRisk_SCL/data/raw/Seattle_City_Light_Lines_-5298229565165338530/Seattle_City_Light_Lines.shp`
- **Rows:** 147,538
- **CRS:** PROJCS["NAD83(HARN) / Washington North (ftUS)",GEOGCS["NAD83(HARN)",DATUM["NAD83_High_Accuracy_Reference_Network",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],AUTHORITY["EPSG","6152"]],PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433]],PROJECTION["Lambert_Conformal_Conic_2SP"],PARAMETER["latitude_of_origin",47],PARAMETER["central_meridian",-120.833333333333],PARAMETER["standard_parallel_1",47.5],PARAMETER["standard_parallel_2",48.7333333333333],PARAMETER["false_easting",1640416.66666667],PARAMETER["false_northing",0],UNIT["US survey foot",0.304800609601219,AUTHORITY["EPSG","9003"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]
- **Geometry:** ['LineString', 'MultiLineString']
- **Columns:** ['SUBTYPECD', 'ConductorT', 'F_GEOMETRY', 'geometry']

#### city_light_poles
- **Path:** `/Users/moses/Desktop/VegetationRisk_SCL/data/raw/Seattle_City_Light_Poles_8609399433741543208/SCL_Poles.shp`
- **Rows:** 101,269
- **CRS:** PROJCS["NAD83(HARN) / Washington North (ftUS)",GEOGCS["NAD83(HARN)",DATUM["NAD83_High_Accuracy_Reference_Network",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],AUTHORITY["EPSG","6152"]],PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433]],PROJECTION["Lambert_Conformal_Conic_2SP"],PARAMETER["latitude_of_origin",47],PARAMETER["central_meridian",-120.833333333333],PARAMETER["standard_parallel_1",47.5],PARAMETER["standard_parallel_2",48.7333333333333],PARAMETER["false_easting",1640416.66666667],PARAMETER["false_northing",0],UNIT["US survey foot",0.304800609601219,AUTHORITY["EPSG","9003"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]
- **Geometry:** ['Point']
- **Columns:** ['SUBTYPECD', 'HEIGHT', 'ASSET_ID', 'HasStreetl', 'Field', 'geometry']

#### fire_stations
- **Path:** `/Users/moses/Desktop/VegetationRisk_SCL/data/raw/Fire_Stations_4483352705992436260/Fire_Station.shp`
- **Rows:** 36
- **CRS:** PROJCS["NAD83(HARN) / Washington North (ftUS)",GEOGCS["NAD83(HARN)",DATUM["NAD83_High_Accuracy_Reference_Network",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],AUTHORITY["EPSG","6152"]],PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433]],PROJECTION["Lambert_Conformal_Conic_2SP"],PARAMETER["latitude_of_origin",47],PARAMETER["central_meridian",-120.833333333333],PARAMETER["standard_parallel_1",47.5],PARAMETER["standard_parallel_2",48.7333333333333],PARAMETER["false_easting",1640416.66666667],PARAMETER["false_northing",0],UNIT["US survey foot",0.304800609601219,AUTHORITY["EPSG","9003"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]
- **Geometry:** ['Point']
- **Columns:** ['STNID', 'ADDRESS', 'SE_ANNO_CA', 'geometry']

#### hospitals
- **Path:** `/Users/moses/Desktop/VegetationRisk_SCL/data/raw/Hospital_-319877742627952756/Hospital.shp`
- **Rows:** 19
- **CRS:** PROJCS["NAD83(HARN) / Washington North (ftUS)",GEOGCS["NAD83(HARN)",DATUM["NAD83_High_Accuracy_Reference_Network",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],AUTHORITY["EPSG","6152"]],PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433]],PROJECTION["Lambert_Conformal_Conic_2SP"],PARAMETER["latitude_of_origin",47],PARAMETER["central_meridian",-120.833333333333],PARAMETER["standard_parallel_1",47.5],PARAMETER["standard_parallel_2",48.7333333333333],PARAMETER["false_easting",1640416.66666667],PARAMETER["false_northing",0],UNIT["US survey foot",0.304800609601219,AUTHORITY["EPSG","9003"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]
- **Geometry:** ['Point']
- **Columns:** ['FACILITY', 'ADDRESS', 'SE_ANNO_CA', 'CITY', 'ACUTE_CARE', 'GIS_EDT_DT', 'URL', 'TELEPHONE', 'GlobalID', 'geometry']

#### neighborhoods
- **Path:** `/Users/moses/Desktop/VegetationRisk_SCL/data/raw/Neighborhood_Map_Atlas_Neighborhoods/Neighborhood_Map_Atlas_Neighborhoods.shp`
- **Rows:** 94
- **CRS:** EPSG:2926
- **Geometry:** ['Polygon', 'MultiPolygon']
- **Columns:** ['OBJECTID', 'L_HOOD', 'S_HOOD', 'S_HOOD_ALT', 'Shape__Are', 'Shape__Len', 'geometry']


---

## 02_prep_data.py
**Run time:** 2026-02-01 19:32:22

### Actions
- Filtered power lines to overhead only (ConductorT = 'OH')
- Merged fire stations (36) and hospitals (19) into critical_facilities
- Standardized all layers to EPSG:2926

### Results
| Output | Rows | File |
|--------|------|------|
| Overhead lines | 109,187 | overhead_lines.gpkg |
| Critical facilities | 55 | critical_facilities.gpkg |
| Neighborhoods | 94 | neighborhoods.gpkg |

Total overhead line length: 1624.4 miles


---

## 03_buffer_analysis.py
**Run time:** 2026-02-01 19:32:53

### Actions
- Created 15-foot buffer around each overhead line segment
- Repaired 0 invalid geometries

### Results
| Metric | Value |
|--------|-------|
| Segments buffered | 109,187 |
| Buffer distance | 15 feet |
| Total buffer area | 7681.5 acres |
| Avg buffer area | 3,065 sq ft |

Output: `line_buffers.gpkg`

