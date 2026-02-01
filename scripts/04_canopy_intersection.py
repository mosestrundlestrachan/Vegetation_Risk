"""
04_canopy_intersection.py
Vegetation-Infrastructure Conflict Prioritization Model
Seattle City Light Portfolio Project

This script calculates vegetation load for each line segment:
- Intersects tree canopy with line buffers
- Calculates canopy area (sq ft) within each buffer
- Normalizes by segment length: canopy_sqft_per_linear_ft

Note: This is computationally intensive due to large tree canopy dataset (~400K polygons)
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
import warnings

# Suppress pandas fragmentation warning
warnings.filterwarnings('ignore', category=pd.errors.PerformanceWarning)

# =============================================================================
# Configuration
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DOCS_DIR = PROJECT_ROOT / "docs"

# Target CRS
TARGET_CRS = "EPSG:2926"

# Tree canopy path
CANOPY_PATH = RAW_DATA_DIR / "TreeCanopy_Seattle_2021_-5593313463288605630" / "TreeCanopy_2021_Seattle.shp"

# Processing chunk size (to manage memory)
CHUNK_SIZE = 5000

# =============================================================================
# Functions
# =============================================================================

def load_and_prep_canopy(canopy_path: Path) -> gpd.GeoDataFrame:
    """
    Load tree canopy data and prepare for analysis.
    - Repair invalid geometries
    - Reproject to target CRS
    """
    print("Loading tree canopy data (this may take a moment)...")
    canopy = gpd.read_file(canopy_path)
    print(f"  Loaded {len(canopy):,} canopy polygons")

    # Reproject if needed
    if canopy.crs.to_string() != TARGET_CRS:
        print(f"  Reprojecting to {TARGET_CRS}...")
        canopy = canopy.to_crs(TARGET_CRS)

    # Repair invalid geometries
    invalid_count = (~canopy.geometry.is_valid).sum()
    if invalid_count > 0:
        print(f"  Repairing {invalid_count} invalid geometries...")
        canopy['geometry'] = canopy.geometry.buffer(0)

    return canopy


def calculate_canopy_intersection_chunked(buffers: gpd.GeoDataFrame,
                                          canopy: gpd.GeoDataFrame,
                                          chunk_size: int = CHUNK_SIZE) -> gpd.GeoDataFrame:
    """
    Calculate canopy area within each buffer using spatial index and chunked processing.

    This approach is more memory-efficient for large datasets.
    """
    print(f"\nCalculating canopy intersections (chunk size: {chunk_size})...")

    # Build spatial index on canopy
    print("  Building spatial index on tree canopy...")
    canopy_sindex = canopy.sindex

    # Initialize results column
    canopy_areas = []

    # Process in chunks with progress bar
    n_chunks = (len(buffers) + chunk_size - 1) // chunk_size

    for i in tqdm(range(0, len(buffers), chunk_size), desc="Processing buffers", total=n_chunks):
        chunk = buffers.iloc[i:i+chunk_size]

        for idx, row in chunk.iterrows():
            buffer_geom = row.geometry

            # Find potentially intersecting canopy polygons using spatial index
            possible_idx = list(canopy_sindex.intersection(buffer_geom.bounds))

            if len(possible_idx) == 0:
                canopy_areas.append(0.0)
                continue

            # Get candidate polygons
            candidates = canopy.iloc[possible_idx]

            # Calculate actual intersection area
            try:
                intersections = candidates.geometry.intersection(buffer_geom)
                total_canopy_area = intersections.area.sum()
                canopy_areas.append(total_canopy_area)
            except Exception:
                canopy_areas.append(0.0)

    return canopy_areas


def main():
    print("\n" + "="*60)
    print("04_CANOPY_INTERSECTION - Calculate Vegetation Load")
    print("="*60)

    # Load line buffers
    print("\nLoading line buffers...")
    buffers_path = PROCESSED_DIR / "line_buffers.gpkg"
    buffers = gpd.read_file(buffers_path)
    print(f"  Loaded {len(buffers):,} buffered segments")

    # Load tree canopy
    canopy = load_and_prep_canopy(CANOPY_PATH)

    # Calculate canopy intersection
    canopy_areas = calculate_canopy_intersection_chunked(buffers, canopy)

    # Add results to buffers
    buffers['canopy_area_sqft'] = canopy_areas

    # Calculate normalized vegetation load
    # canopy_sqft_per_linear_ft = canopy_area / segment_length
    buffers['canopy_sqft_per_ft'] = buffers['canopy_area_sqft'] / buffers['length_ft']

    # Handle any division issues
    buffers['canopy_sqft_per_ft'] = buffers['canopy_sqft_per_ft'].fillna(0)

    # Export results
    print("\nExporting results...")
    output_path = PROCESSED_DIR / "lines_with_canopy.gpkg"
    buffers.to_file(output_path, driver="GPKG")
    print(f"  Saved: {output_path}")

    # Summary statistics
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    segments_with_canopy = (buffers['canopy_area_sqft'] > 0).sum()
    pct_with_canopy = segments_with_canopy / len(buffers) * 100

    print(f"  Total segments: {len(buffers):,}")
    print(f"  Segments with canopy: {segments_with_canopy:,} ({pct_with_canopy:.1f}%)")
    print(f"  Total canopy area in buffers: {buffers['canopy_area_sqft'].sum() / 43560:.1f} acres")
    print(f"\n  Canopy per linear foot statistics:")
    print(f"    Mean: {buffers['canopy_sqft_per_ft'].mean():.2f} sq ft/ft")
    print(f"    Median: {buffers['canopy_sqft_per_ft'].median():.2f} sq ft/ft")
    print(f"    Max: {buffers['canopy_sqft_per_ft'].max():.2f} sq ft/ft")
    print(f"    Std: {buffers['canopy_sqft_per_ft'].std():.2f} sq ft/ft")

    # Update process log
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_content = f"""
---

## 04_canopy_intersection.py
**Run time:** {timestamp}

### Actions
- Loaded tree canopy data ({len(canopy):,} polygons)
- Calculated canopy area within each 15-foot line buffer
- Normalized by segment length (canopy_sqft_per_ft)

### Results
| Metric | Value |
|--------|-------|
| Total segments | {len(buffers):,} |
| Segments with canopy | {segments_with_canopy:,} ({pct_with_canopy:.1f}%) |
| Total canopy in buffers | {buffers['canopy_area_sqft'].sum() / 43560:.1f} acres |
| Mean canopy/ft | {buffers['canopy_sqft_per_ft'].mean():.2f} sq ft/ft |
| Max canopy/ft | {buffers['canopy_sqft_per_ft'].max():.2f} sq ft/ft |

Output: `lines_with_canopy.gpkg`

"""
    with open(DOCS_DIR / "process_log.md", "a") as f:
        f.write(log_content)
    print("\nProcess log updated.")

    return buffers


if __name__ == "__main__":
    main()
