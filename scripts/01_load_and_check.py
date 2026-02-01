"""
01_load_and_check.py
Vegetation-Infrastructure Conflict Prioritization Model
Seattle City Light Portfolio Project

This script loads all shapefiles and validates:
- CRS consistency across layers
- Row counts and column names
- Geometry validity
"""

import geopandas as gpd
from pathlib import Path
from datetime import datetime

# =============================================================================
# Configuration
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
DOCS_DIR = PROJECT_ROOT / "docs"

# Shapefile paths (using actual folder names)
DATA_PATHS = {
    "tree_canopy": RAW_DATA_DIR / "TreeCanopy_Seattle_2021_-5593313463288605630" / "TreeCanopy_2021_Seattle.shp",
    "city_light_lines": RAW_DATA_DIR / "Seattle_City_Light_Lines_-5298229565165338530" / "Seattle_City_Light_Lines.shp",
    "city_light_poles": RAW_DATA_DIR / "Seattle_City_Light_Poles_8609399433741543208" / "SCL_Poles.shp",
    "fire_stations": RAW_DATA_DIR / "Fire_Stations_4483352705992436260" / "Fire_Station.shp",
    "hospitals": RAW_DATA_DIR / "Hospital_-319877742627952756" / "Hospital.shp",
    "neighborhoods": RAW_DATA_DIR / "Neighborhood_Map_Atlas_Neighborhoods" / "Neighborhood_Map_Atlas_Neighborhoods.shp",
}

# =============================================================================
# Functions
# =============================================================================

def load_and_check_layer(name: str, path: Path) -> dict:
    """Load a shapefile and return diagnostic information."""
    print(f"\n{'='*60}")
    print(f"Loading: {name}")
    print(f"{'='*60}")

    info = {"name": name, "path": str(path), "issues": []}

    # Check if file exists
    if not path.exists():
        info["issues"].append(f"FILE NOT FOUND: {path}")
        print(f"  ERROR: File not found!")
        return info

    # Load the shapefile
    try:
        gdf = gpd.read_file(path)
    except Exception as e:
        info["issues"].append(f"LOAD ERROR: {e}")
        print(f"  ERROR: Could not load file - {e}")
        return info

    # Basic info
    info["row_count"] = len(gdf)
    info["crs"] = str(gdf.crs) if gdf.crs else "None"
    info["columns"] = list(gdf.columns)
    info["geometry_type"] = gdf.geometry.geom_type.unique().tolist()

    print(f"  Rows: {info['row_count']:,}")
    print(f"  CRS: {info['crs']}")
    print(f"  Geometry type(s): {info['geometry_type']}")
    print(f"  Columns: {info['columns']}")

    # Check for invalid geometries
    invalid_count = (~gdf.geometry.is_valid).sum()
    if invalid_count > 0:
        info["issues"].append(f"Invalid geometries: {invalid_count}")
        print(f"  WARNING: {invalid_count} invalid geometries found")

    # Check for null geometries
    null_count = gdf.geometry.isna().sum()
    if null_count > 0:
        info["issues"].append(f"Null geometries: {null_count}")
        print(f"  WARNING: {null_count} null geometries found")

    # Check CRS
    if gdf.crs is None:
        info["issues"].append("No CRS defined")
        print(f"  WARNING: No CRS defined!")

    # Sample of first few rows (non-geometry columns)
    non_geom_cols = [c for c in gdf.columns if c != 'geometry']
    if non_geom_cols:
        print(f"\n  Sample data (first 3 rows):")
        print(gdf[non_geom_cols].head(3).to_string(index=False))

    return info


def write_process_log(results: list, log_path: Path):
    """Write results to process log."""
    log_path.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_path, "w") as f:
        f.write("# Process Log - Vegetation Risk Model\n\n")
        f.write(f"## 01_load_and_check.py\n")
        f.write(f"**Run time:** {timestamp}\n\n")
        f.write("### Summary\n\n")

        # Summary table
        f.write("| Layer | Rows | CRS | Issues |\n")
        f.write("|-------|------|-----|--------|\n")
        for r in results:
            issues = "; ".join(r.get("issues", [])) if r.get("issues") else "None"
            f.write(f"| {r['name']} | {r.get('row_count', 'N/A'):,} | {r.get('crs', 'N/A')[:30]} | {issues} |\n")

        f.write("\n### Details\n\n")
        for r in results:
            f.write(f"#### {r['name']}\n")
            f.write(f"- **Path:** `{r['path']}`\n")
            f.write(f"- **Rows:** {r.get('row_count', 'N/A'):,}\n")
            f.write(f"- **CRS:** {r.get('crs', 'N/A')}\n")
            f.write(f"- **Geometry:** {r.get('geometry_type', 'N/A')}\n")
            f.write(f"- **Columns:** {r.get('columns', 'N/A')}\n")
            if r.get("issues"):
                f.write(f"- **Issues:** {', '.join(r['issues'])}\n")
            f.write("\n")

    print(f"\nProcess log written to: {log_path}")


# =============================================================================
# Main
# =============================================================================

def main():
    print("\n" + "="*60)
    print("VEGETATION RISK MODEL - DATA VALIDATION")
    print("Seattle City Light Portfolio Project")
    print("="*60)

    results = []
    crs_values = set()

    # Load and check each layer
    for name, path in DATA_PATHS.items():
        info = load_and_check_layer(name, path)
        results.append(info)
        if info.get("crs") and info["crs"] != "None":
            crs_values.add(info["crs"])

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    print(f"\nTotal layers loaded: {len(results)}")
    print(f"Unique CRS values found: {len(crs_values)}")

    if len(crs_values) == 1:
        print(f"  ✓ All layers share the same CRS: {list(crs_values)[0][:50]}...")
    elif len(crs_values) > 1:
        print(f"  ✗ WARNING: Multiple CRS values detected!")
        for crs in crs_values:
            print(f"    - {crs[:50]}...")

    # Check for issues
    all_issues = []
    for r in results:
        if r.get("issues"):
            for issue in r["issues"]:
                all_issues.append(f"{r['name']}: {issue}")

    if all_issues:
        print(f"\nIssues found ({len(all_issues)}):")
        for issue in all_issues:
            print(f"  - {issue}")
    else:
        print("\n✓ No issues found - data is ready for processing")

    # Write process log
    log_path = DOCS_DIR / "process_log.md"
    write_process_log(results, log_path)

    return results


if __name__ == "__main__":
    main()
