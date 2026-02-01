"""
05_proximity_analysis.py
Vegetation-Infrastructure Conflict Prioritization Model
Seattle City Light Portfolio Project

This script calculates proximity to critical facilities:
- Calculates distance from each line segment centroid to nearest critical facility
- Classifies into proximity scores:
  - < 500 ft = 3 (highest priority)
  - 500-1500 ft = 2
  - > 1500 ft = 1
"""

import geopandas as gpd
import numpy as np
from pathlib import Path
from datetime import datetime
from tqdm import tqdm

# =============================================================================
# Configuration
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DOCS_DIR = PROJECT_ROOT / "docs"

# Proximity thresholds (feet)
PROXIMITY_THRESHOLDS = {
    'high': 500,     # < 500 ft = score 3
    'medium': 1500,  # 500-1500 ft = score 2
                     # > 1500 ft = score 1
}

# =============================================================================
# Functions
# =============================================================================

def classify_proximity(distance: float) -> int:
    """
    Classify distance into proximity score.

    Args:
        distance: Distance in feet

    Returns:
        Score: 3 (high priority), 2 (medium), 1 (low)
    """
    if distance < PROXIMITY_THRESHOLDS['high']:
        return 3
    elif distance < PROXIMITY_THRESHOLDS['medium']:
        return 2
    else:
        return 1


def calculate_proximity_to_facilities(lines: gpd.GeoDataFrame,
                                      facilities: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Calculate distance from each line segment centroid to nearest critical facility.

    Args:
        lines: GeoDataFrame with line/polygon geometries
        facilities: GeoDataFrame with critical facility points

    Returns:
        lines GeoDataFrame with added proximity_dist_ft and proximity_score columns
    """
    print("\nCalculating proximity to critical facilities...")

    # Get centroids of line segments (or buffer polygons)
    lines = lines.copy()

    # Calculate centroid once
    print("  Calculating segment centroids...")
    centroids = lines.geometry.centroid

    # Use sjoin_nearest for efficient nearest neighbor calculation
    print("  Finding nearest facility for each segment...")

    # Create a temporary GeoDataFrame with centroids
    centroids_gdf = gpd.GeoDataFrame(
        {'segment_idx': range(len(centroids))},
        geometry=centroids,
        crs=lines.crs
    )

    # Use sjoin_nearest to find nearest facility
    nearest = gpd.sjoin_nearest(
        centroids_gdf,
        facilities[['geometry', 'facility_type']],
        how='left',
        distance_col='proximity_dist_ft'
    )

    # Handle any duplicates (take first match)
    nearest = nearest.drop_duplicates(subset='segment_idx', keep='first')
    nearest = nearest.sort_values('segment_idx').reset_index(drop=True)

    # Add results to lines
    lines['proximity_dist_ft'] = nearest['proximity_dist_ft'].values
    lines['nearest_facility_type'] = nearest['facility_type'].values

    # Classify proximity scores using vectorized operations
    lines['proximity_score'] = np.where(
        lines['proximity_dist_ft'] < PROXIMITY_THRESHOLDS['high'], 3,
        np.where(lines['proximity_dist_ft'] < PROXIMITY_THRESHOLDS['medium'], 2, 1)
    )

    return lines


def main():
    print("\n" + "="*60)
    print("05_PROXIMITY_ANALYSIS - Critical Facility Proximity")
    print("="*60)

    # Load data
    print("\nLoading data...")
    lines_path = PROCESSED_DIR / "lines_with_canopy.gpkg"
    facilities_path = PROCESSED_DIR / "critical_facilities.gpkg"

    lines = gpd.read_file(lines_path)
    facilities = gpd.read_file(facilities_path)

    print(f"  Loaded {len(lines):,} line segments")
    print(f"  Loaded {len(facilities):,} critical facilities")

    # Calculate proximity
    lines = calculate_proximity_to_facilities(lines, facilities)

    # Export results
    print("\nExporting results...")
    output_path = PROCESSED_DIR / "lines_with_proximity.gpkg"
    lines.to_file(output_path, driver="GPKG")
    print(f"  Saved: {output_path}")

    # Summary statistics
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    score_counts = lines['proximity_score'].value_counts().sort_index()
    print(f"\n  Proximity Score Distribution:")
    print(f"    Score 3 (< 500 ft):     {score_counts.get(3, 0):,} segments ({score_counts.get(3, 0)/len(lines)*100:.1f}%)")
    print(f"    Score 2 (500-1500 ft):  {score_counts.get(2, 0):,} segments ({score_counts.get(2, 0)/len(lines)*100:.1f}%)")
    print(f"    Score 1 (> 1500 ft):    {score_counts.get(1, 0):,} segments ({score_counts.get(1, 0)/len(lines)*100:.1f}%)")

    print(f"\n  Distance Statistics:")
    print(f"    Mean distance: {lines['proximity_dist_ft'].mean():,.0f} ft")
    print(f"    Median distance: {lines['proximity_dist_ft'].median():,.0f} ft")
    print(f"    Min distance: {lines['proximity_dist_ft'].min():,.0f} ft")
    print(f"    Max distance: {lines['proximity_dist_ft'].max():,.0f} ft")

    print(f"\n  Nearest Facility Type:")
    type_counts = lines['nearest_facility_type'].value_counts()
    for ftype, count in type_counts.items():
        print(f"    {ftype}: {count:,} segments")

    # Update process log
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_content = f"""
---

## 05_proximity_analysis.py
**Run time:** {timestamp}

### Actions
- Calculated distance from each line segment centroid to nearest critical facility
- Classified proximity into scores (3 = < 500 ft, 2 = 500-1500 ft, 1 = > 1500 ft)

### Results

**Proximity Score Distribution:**
| Score | Distance | Count | Percentage |
|-------|----------|-------|------------|
| 3 (High) | < 500 ft | {score_counts.get(3, 0):,} | {score_counts.get(3, 0)/len(lines)*100:.1f}% |
| 2 (Medium) | 500-1500 ft | {score_counts.get(2, 0):,} | {score_counts.get(2, 0)/len(lines)*100:.1f}% |
| 1 (Low) | > 1500 ft | {score_counts.get(1, 0):,} | {score_counts.get(1, 0)/len(lines)*100:.1f}% |

**Distance Statistics:**
- Mean: {lines['proximity_dist_ft'].mean():,.0f} ft
- Median: {lines['proximity_dist_ft'].median():,.0f} ft

Output: `lines_with_proximity.gpkg`

"""
    with open(DOCS_DIR / "process_log.md", "a") as f:
        f.write(log_content)
    print("\nProcess log updated.")

    return lines


if __name__ == "__main__":
    main()
