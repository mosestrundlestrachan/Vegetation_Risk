"""
02_prep_data.py
Vegetation-Infrastructure Conflict Prioritization Model
Seattle City Light Portfolio Project

This script prepares data for analysis:
- Filters City Light Lines to overhead only (ConductorT = 'OH')
- Merges Fire Stations and Hospitals into critical_facilities layer
- Standardizes CRS across all layers
- Exports cleaned layers to data/processed
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path
from datetime import datetime

# =============================================================================
# Configuration
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DOCS_DIR = PROJECT_ROOT / "docs"

# Target CRS - Washington North State Plane (US Feet)
TARGET_CRS = "EPSG:2926"

# Shapefile paths
DATA_PATHS = {
    "city_light_lines": RAW_DATA_DIR / "Seattle_City_Light_Lines_-5298229565165338530" / "Seattle_City_Light_Lines.shp",
    "fire_stations": RAW_DATA_DIR / "Fire_Stations_4483352705992436260" / "Fire_Station.shp",
    "hospitals": RAW_DATA_DIR / "Hospital_-319877742627952756" / "Hospital.shp",
    "neighborhoods": RAW_DATA_DIR / "Neighborhood_Map_Atlas_Neighborhoods" / "Neighborhood_Map_Atlas_Neighborhoods.shp",
}

# =============================================================================
# Functions
# =============================================================================

def filter_overhead_lines(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Filter power lines to overhead only.

    Based on 01_load_and_check.py, the attribute is:
    - ConductorT = 'OH' for overhead lines
    """
    print("\nFiltering to overhead lines only...")
    print(f"  Original count: {len(gdf):,}")

    # Check available values
    if 'ConductorT' in gdf.columns:
        print(f"  ConductorT values: {gdf['ConductorT'].unique()}")
        overhead = gdf[gdf['ConductorT'] == 'OH'].copy()
    else:
        print("  WARNING: ConductorT column not found, using all lines")
        overhead = gdf.copy()

    print(f"  Filtered count: {len(overhead):,}")
    print(f"  Removed: {len(gdf) - len(overhead):,} underground/other lines")

    # Add unique segment ID
    overhead = overhead.reset_index(drop=True)
    overhead['segment_id'] = range(len(overhead))

    # Calculate segment length (CRS is in feet)
    overhead['length_ft'] = overhead.geometry.length

    return overhead


def create_critical_facilities(fire_stations: gpd.GeoDataFrame,
                               hospitals: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Merge fire stations and hospitals into single critical facilities layer.
    """
    print("\nCreating critical facilities layer...")

    # Prepare fire stations
    fs = fire_stations[['geometry']].copy()
    fs['facility_type'] = 'fire_station'
    fs['facility_name'] = fire_stations['STNID'] if 'STNID' in fire_stations.columns else 'Fire Station'

    # Prepare hospitals
    hosp = hospitals[['geometry']].copy()
    hosp['facility_type'] = 'hospital'
    hosp['facility_name'] = hospitals['FACILITY'] if 'FACILITY' in hospitals.columns else 'Hospital'

    # Combine
    critical = pd.concat([fs, hosp], ignore_index=True)
    critical = gpd.GeoDataFrame(critical, crs=fire_stations.crs)

    print(f"  Fire stations: {len(fs):,}")
    print(f"  Hospitals: {len(hosp):,}")
    print(f"  Total critical facilities: {len(critical):,}")

    return critical


def standardize_crs(gdf: gpd.GeoDataFrame, name: str) -> gpd.GeoDataFrame:
    """Ensure GeoDataFrame uses target CRS."""
    if gdf.crs is None:
        print(f"  {name}: No CRS, setting to {TARGET_CRS}")
        gdf = gdf.set_crs(TARGET_CRS)
    elif gdf.crs.to_string() != TARGET_CRS:
        print(f"  {name}: Reprojecting to {TARGET_CRS}")
        gdf = gdf.to_crs(TARGET_CRS)
    else:
        print(f"  {name}: CRS OK")
    return gdf


def update_process_log(log_path: Path, content: str):
    """Append to process log."""
    with open(log_path, "a") as f:
        f.write(content)


# =============================================================================
# Main
# =============================================================================

def main():
    print("\n" + "="*60)
    print("02_PREP_DATA - Data Preparation")
    print("="*60)

    # Ensure output directory exists
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Load data
    print("\nLoading data...")
    lines = gpd.read_file(DATA_PATHS["city_light_lines"])
    fire_stations = gpd.read_file(DATA_PATHS["fire_stations"])
    hospitals = gpd.read_file(DATA_PATHS["hospitals"])
    neighborhoods = gpd.read_file(DATA_PATHS["neighborhoods"])

    # Standardize CRS
    print("\nStandardizing CRS...")
    lines = standardize_crs(lines, "city_light_lines")
    fire_stations = standardize_crs(fire_stations, "fire_stations")
    hospitals = standardize_crs(hospitals, "hospitals")
    neighborhoods = standardize_crs(neighborhoods, "neighborhoods")

    # Filter to overhead lines
    overhead_lines = filter_overhead_lines(lines)

    # Create critical facilities layer
    critical_facilities = create_critical_facilities(fire_stations, hospitals)
    critical_facilities = standardize_crs(critical_facilities, "critical_facilities")

    # Prepare neighborhoods (standardize column names)
    print("\nPreparing neighborhoods...")
    if 'S_HOOD' in neighborhoods.columns:
        neighborhoods = neighborhoods.rename(columns={'S_HOOD': 'neighborhood'})
    print(f"  Neighborhoods: {len(neighborhoods):,}")

    # Export to GeoPackage
    print("\nExporting to GeoPackage...")

    overhead_path = PROCESSED_DIR / "overhead_lines.gpkg"
    overhead_lines.to_file(overhead_path, driver="GPKG")
    print(f"  Saved: {overhead_path}")

    facilities_path = PROCESSED_DIR / "critical_facilities.gpkg"
    critical_facilities.to_file(facilities_path, driver="GPKG")
    print(f"  Saved: {facilities_path}")

    neighborhoods_path = PROCESSED_DIR / "neighborhoods.gpkg"
    neighborhoods.to_file(neighborhoods_path, driver="GPKG")
    print(f"  Saved: {neighborhoods_path}")

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"  Overhead line segments: {len(overhead_lines):,}")
    print(f"  Critical facilities: {len(critical_facilities):,}")
    print(f"  Neighborhoods: {len(neighborhoods):,}")
    print(f"  Total line length: {overhead_lines['length_ft'].sum() / 5280:.1f} miles")

    # Update process log
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_content = f"""
---

## 02_prep_data.py
**Run time:** {timestamp}

### Actions
- Filtered power lines to overhead only (ConductorT = 'OH')
- Merged fire stations ({len(fire_stations)}) and hospitals ({len(hospitals)}) into critical_facilities
- Standardized all layers to {TARGET_CRS}

### Results
| Output | Rows | File |
|--------|------|------|
| Overhead lines | {len(overhead_lines):,} | overhead_lines.gpkg |
| Critical facilities | {len(critical_facilities):,} | critical_facilities.gpkg |
| Neighborhoods | {len(neighborhoods):,} | neighborhoods.gpkg |

Total overhead line length: {overhead_lines['length_ft'].sum() / 5280:.1f} miles

"""
    update_process_log(DOCS_DIR / "process_log.md", log_content)
    print("\nProcess log updated.")

    return overhead_lines, critical_facilities, neighborhoods


if __name__ == "__main__":
    main()
