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


---

## 04_canopy_intersection.py
**Run time:** 2026-02-01 19:36:50

### Actions
- Loaded tree canopy data (408,646 polygons)
- Calculated canopy area within each 15-foot line buffer
- Normalized by segment length (canopy_sqft_per_ft)

### Results
| Metric | Value |
|--------|-------|
| Total segments | 109,187 |
| Segments with canopy | 73,649 (67.5%) |
| Total canopy in buffers | 1216.8 acres |
| Mean canopy/ft | 45.99 sq ft/ft |
| Max canopy/ft | 13944.35 sq ft/ft |

Output: `lines_with_canopy.gpkg`


---

## 05_proximity_analysis.py
**Run time:** 2026-02-01 19:38:18

### Actions
- Calculated distance from each line segment centroid to nearest critical facility
- Classified proximity into scores (3 = < 500 ft, 2 = 500-1500 ft, 1 = > 1500 ft)

### Results

**Proximity Score Distribution:**
| Score | Distance | Count | Percentage |
|-------|----------|-------|------------|
| 3 (High) | < 500 ft | 1,506 | 1.4% |
| 2 (Medium) | 500-1500 ft | 10,643 | 9.7% |
| 1 (Low) | > 1500 ft | 97,038 | 88.9% |

**Distance Statistics:**
- Mean: 5,026 ft
- Median: 3,793 ft

Output: `lines_with_proximity.gpkg`


---

## 06_risk_scoring.py
**Run time:** 2026-02-01 19:39:04

### Actions
- Normalized all risk factors to 0-1 scale
- Applied weighted scoring: Vegetation 50%, Proximity 30%, Length 20%
- Classified into risk tiers based on percentiles

### Risk Score Statistics
| Metric | Value |
|--------|-------|
| Mean | 0.1305 |
| Median | 0.1233 |
| Std Dev | 0.0392 |
| Min | 0.1000 |
| Max | 0.8000 |

### Risk Tier Distribution
| Tier | Segments | Percentage | Miles |
|------|----------|------------|-------|
| High | 21,838 | 20.0% | 519.6 |
| Medium | 43,674 | 40.0% | 997.4 |
| Low | 43,675 | 40.0% | 107.5 |

Output: `scored_segments.gpkg`


---

## 07_summarize.py
**Run time:** 2026-02-01 19:39:47

### Actions
- Spatially joined segments to neighborhoods
- Calculated per-neighborhood statistics
- Exported top 25 priority segments

### Outputs
- `neighborhood_summary.csv` (92 neighborhoods)
- `priority_segments.csv` (25 segments)

### Top 5 High-Risk Neighborhoods
| Neighborhood | Total Miles | High Risk Miles | % High Risk |
|-------------|-------------|-----------------|-------------|
| First Hill | 3.3 | 2.9 | 85.0% |
| Yesler Terrace | 3.0 | 2.5 | 81.1% |
| Laurelhurst | 3.0 | 2.0 | 57.9% |
| Harrison/Denny-Blaine | 3.7 | 2.2 | 56.5% |
| Minor | 14.5 | 8.8 | 54.0% |

### Citywide Summary
- Total overhead line miles: 1624.4
- High risk miles: 519.6 (32.0%)


---

## 08_visualize.py
**Run time:** 2026-02-01 19:40:52

### Actions
- Created citywide risk map (all segments colored by tier)
- Created detail map of highest-risk neighborhood (First Hill)

### Outputs
- `citywide_risk_map.png` - Overview of all Seattle area
- `detail_high_risk_area.png` - Zoomed view of First Hill

