"""
03_buffer_analysis.py
Vegetation-Infrastructure Conflict Prioritization Model
Seattle City Light Portfolio Project

This script creates buffer zones around overhead power lines:
- 15-foot buffer representing vegetation clearance zone
- Repairs any invalid geometries
- Exports buffered lines to data/processed
"""

import geopandas as gpd
from pathlib import Path
from datetime import datetime

# =============================================================================
# Configuration
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DOCS_DIR = PROJECT_ROOT / "docs"

# Buffer distance in feet (CRS is in US feet)
BUFFER_DISTANCE_FT = 15

# =============================================================================
# Functions
# =============================================================================

def repair_geometries(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Repair invalid geometries using buffer(0) technique."""
    invalid_count = (~gdf.geometry.is_valid).sum()

    if invalid_count > 0:
        print(f"  Repairing {invalid_count} invalid geometries...")
        gdf['geometry'] = gdf.geometry.buffer(0)

        # Verify repair
        still_invalid = (~gdf.geometry.is_valid).sum()
        if still_invalid > 0:
            print(f"  WARNING: {still_invalid} geometries still invalid after repair")
        else:
            print(f"  All geometries now valid")

    return gdf


def create_line_buffers(gdf: gpd.GeoDataFrame, buffer_distance: float) -> gpd.GeoDataFrame:
    """
    Create buffer polygons around line segments.

    Args:
        gdf: GeoDataFrame with LineString geometries
        buffer_distance: Buffer distance in CRS units (feet)

    Returns:
        GeoDataFrame with Polygon geometries (buffered lines)
    """
    print(f"\nCreating {buffer_distance}-foot buffers...")

    # Create buffers
    buffered = gdf.copy()
    buffered['geometry'] = gdf.geometry.buffer(buffer_distance)

    # Calculate buffer area
    buffered['buffer_area_sqft'] = buffered.geometry.area

    print(f"  Buffered {len(buffered):,} line segments")
    print(f"  Average buffer area: {buffered['buffer_area_sqft'].mean():,.0f} sq ft")

    return buffered


def update_process_log(log_path: Path, content: str):
    """Append to process log."""
    with open(log_path, "a") as f:
        f.write(content)


# =============================================================================
# Main
# =============================================================================

def main():
    print("\n" + "="*60)
    print("03_BUFFER_ANALYSIS - Create Vegetation Clearance Zones")
    print("="*60)

    # Load overhead lines
    print("\nLoading overhead lines...")
    lines_path = PROCESSED_DIR / "overhead_lines.gpkg"
    lines = gpd.read_file(lines_path)
    print(f"  Loaded {len(lines):,} line segments")

    # Repair any invalid geometries
    print("\nChecking geometry validity...")
    invalid_count = (~lines.geometry.is_valid).sum()
    print(f"  Invalid geometries: {invalid_count}")
    if invalid_count > 0:
        lines = repair_geometries(lines)

    # Create buffers
    buffered_lines = create_line_buffers(lines, BUFFER_DISTANCE_FT)

    # Export
    print("\nExporting buffered lines...")
    output_path = PROCESSED_DIR / "line_buffers.gpkg"
    buffered_lines.to_file(output_path, driver="GPKG")
    print(f"  Saved: {output_path}")

    # Summary statistics
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"  Buffer distance: {BUFFER_DISTANCE_FT} feet")
    print(f"  Segments buffered: {len(buffered_lines):,}")
    print(f"  Total buffer area: {buffered_lines['buffer_area_sqft'].sum() / 43560:.1f} acres")
    print(f"  Min buffer area: {buffered_lines['buffer_area_sqft'].min():,.0f} sq ft")
    print(f"  Max buffer area: {buffered_lines['buffer_area_sqft'].max():,.0f} sq ft")

    # Update process log
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_content = f"""
---

## 03_buffer_analysis.py
**Run time:** {timestamp}

### Actions
- Created {BUFFER_DISTANCE_FT}-foot buffer around each overhead line segment
- Repaired {invalid_count} invalid geometries

### Results
| Metric | Value |
|--------|-------|
| Segments buffered | {len(buffered_lines):,} |
| Buffer distance | {BUFFER_DISTANCE_FT} feet |
| Total buffer area | {buffered_lines['buffer_area_sqft'].sum() / 43560:.1f} acres |
| Avg buffer area | {buffered_lines['buffer_area_sqft'].mean():,.0f} sq ft |

Output: `line_buffers.gpkg`

"""
    update_process_log(DOCS_DIR / "process_log.md", log_content)
    print("\nProcess log updated.")

    return buffered_lines


if __name__ == "__main__":
    main()
