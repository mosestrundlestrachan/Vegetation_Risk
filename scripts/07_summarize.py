"""
07_summarize.py
Vegetation-Infrastructure Conflict Prioritization Model
Seattle City Light Portfolio Project

This script creates summary outputs:
- Spatial join segments to neighborhoods
- Calculate per neighborhood: total line miles, high-risk miles, % high-risk
- Export neighborhood_summary.csv
- Export top 25 priority segments to priority_segments.csv
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path
from datetime import datetime

# =============================================================================
# Configuration
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
DOCS_DIR = PROJECT_ROOT / "docs"

# Number of top priority segments to export
TOP_N_SEGMENTS = 25

# =============================================================================
# Functions
# =============================================================================

def aggregate_by_neighborhood(segments: gpd.GeoDataFrame,
                              neighborhoods: gpd.GeoDataFrame) -> pd.DataFrame:
    """
    Spatially join segments to neighborhoods and calculate summary statistics.
    """
    print("\nAggregating by neighborhood...")

    # Spatial join - use segment centroids to assign to neighborhoods
    segments = segments.copy()
    segments['centroid'] = segments.geometry.centroid

    # Create temporary GeoDataFrame with centroids
    centroids_gdf = gpd.GeoDataFrame(
        segments.drop(columns=['geometry']),
        geometry=segments['centroid'],
        crs=segments.crs
    )

    # Spatial join to neighborhoods
    joined = gpd.sjoin(
        centroids_gdf,
        neighborhoods[['geometry', 'neighborhood']],
        how='left',
        predicate='within'
    )

    # Handle segments that didn't fall within any neighborhood (boundary cases)
    null_count = joined['neighborhood'].isna().sum()
    if null_count > 0:
        print(f"  Note: {null_count} segments not within neighborhood boundaries (boundary cases)")
        joined['neighborhood'] = joined['neighborhood'].fillna('Outside City Limits')

    # Calculate statistics by neighborhood
    stats = joined.groupby('neighborhood').agg(
        total_segments=('segment_id', 'count'),
        total_length_ft=('length_ft', 'sum'),
        high_risk_segments=('risk_tier', lambda x: (x == 'High').sum()),
        high_risk_length_ft=('length_ft', lambda x: x[joined.loc[x.index, 'risk_tier'] == 'High'].sum()),
        avg_risk_score=('risk_score', 'mean'),
        max_risk_score=('risk_score', 'max'),
        avg_canopy_per_ft=('canopy_sqft_per_ft', 'mean')
    ).reset_index()

    # Calculate derived metrics
    stats['total_miles'] = stats['total_length_ft'] / 5280
    stats['high_risk_miles'] = stats['high_risk_length_ft'] / 5280
    stats['pct_high_risk'] = (stats['high_risk_segments'] / stats['total_segments'] * 100).round(1)

    # Sort by high risk percentage descending
    stats = stats.sort_values('pct_high_risk', ascending=False)

    return stats, joined


def export_priority_segments(segments: gpd.GeoDataFrame, n: int) -> pd.DataFrame:
    """
    Export top N priority segments with relevant attributes.
    """
    print(f"\nExporting top {n} priority segments...")

    # Get top N by priority rank
    top_segments = segments.nsmallest(n, 'priority_rank').copy()

    # Select and rename columns for export
    export_cols = {
        'segment_id': 'segment_id',
        'priority_rank': 'priority_rank',
        'risk_score': 'risk_score',
        'risk_tier': 'risk_tier',
        'canopy_sqft_per_ft': 'canopy_sqft_per_ft',
        'proximity_score': 'proximity_score',
        'proximity_dist_ft': 'proximity_dist_ft',
        'nearest_facility_type': 'nearest_facility_type',
        'length_ft': 'length_ft'
    }

    # Filter to available columns
    available_cols = {k: v for k, v in export_cols.items() if k in top_segments.columns}
    export_df = top_segments[list(available_cols.keys())].rename(columns=available_cols)

    # Round numeric columns
    numeric_cols = ['risk_score', 'canopy_sqft_per_ft', 'proximity_dist_ft', 'length_ft']
    for col in numeric_cols:
        if col in export_df.columns:
            export_df[col] = export_df[col].round(2)

    return export_df


def main():
    print("\n" + "="*60)
    print("07_SUMMARIZE - Create Summary Outputs")
    print("="*60)

    # Ensure output directory exists
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    # Load data
    print("\nLoading data...")
    segments_path = PROCESSED_DIR / "scored_segments.gpkg"
    neighborhoods_path = PROCESSED_DIR / "neighborhoods.gpkg"

    segments = gpd.read_file(segments_path)
    neighborhoods = gpd.read_file(neighborhoods_path)

    print(f"  Loaded {len(segments):,} scored segments")
    print(f"  Loaded {len(neighborhoods):,} neighborhoods")

    # ==========================================================================
    # Neighborhood Summary
    # ==========================================================================
    neighborhood_stats, joined_segments = aggregate_by_neighborhood(segments, neighborhoods)

    # Export neighborhood summary
    neighborhood_output = OUTPUTS_DIR / "neighborhood_summary.csv"
    neighborhood_stats.to_csv(neighborhood_output, index=False)
    print(f"  Saved: {neighborhood_output}")

    # ==========================================================================
    # Priority Segments
    # ==========================================================================
    priority_df = export_priority_segments(segments, TOP_N_SEGMENTS)

    # Export priority segments
    priority_output = OUTPUTS_DIR / "priority_segments.csv"
    priority_df.to_csv(priority_output, index=False)
    print(f"  Saved: {priority_output}")

    # ==========================================================================
    # Summary statistics
    # ==========================================================================
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    print(f"\n  Neighborhood Summary ({len(neighborhood_stats)} neighborhoods):")
    print(f"\n  Top 10 Neighborhoods by High Risk Percentage:")
    top10_hoods = neighborhood_stats.head(10)[
        ['neighborhood', 'total_miles', 'high_risk_miles', 'pct_high_risk', 'avg_risk_score']
    ].round(2)
    print(top10_hoods.to_string(index=False))

    print(f"\n  Priority Segments (Top {TOP_N_SEGMENTS}):")
    print(f"    Risk scores range: {priority_df['risk_score'].min():.4f} - {priority_df['risk_score'].max():.4f}")
    print(f"    All segments in High tier: {(priority_df['risk_tier'] == 'High').all()}")

    # Citywide summary
    total_miles = segments['length_ft'].sum() / 5280
    high_risk_miles = segments[segments['risk_tier'] == 'High']['length_ft'].sum() / 5280
    pct_high_risk = high_risk_miles / total_miles * 100

    print(f"\n  Citywide Summary:")
    print(f"    Total overhead line miles: {total_miles:.1f}")
    print(f"    High risk miles: {high_risk_miles:.1f} ({pct_high_risk:.1f}%)")

    # Update process log
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_content = f"""
---

## 07_summarize.py
**Run time:** {timestamp}

### Actions
- Spatially joined segments to neighborhoods
- Calculated per-neighborhood statistics
- Exported top {TOP_N_SEGMENTS} priority segments

### Outputs
- `neighborhood_summary.csv` ({len(neighborhood_stats)} neighborhoods)
- `priority_segments.csv` ({TOP_N_SEGMENTS} segments)

### Top 5 High-Risk Neighborhoods
| Neighborhood | Total Miles | High Risk Miles | % High Risk |
|-------------|-------------|-----------------|-------------|
"""
    for _, row in neighborhood_stats.head(5).iterrows():
        log_content += f"| {row['neighborhood']} | {row['total_miles']:.1f} | {row['high_risk_miles']:.1f} | {row['pct_high_risk']:.1f}% |\n"

    log_content += f"""
### Citywide Summary
- Total overhead line miles: {total_miles:.1f}
- High risk miles: {high_risk_miles:.1f} ({pct_high_risk:.1f}%)

"""
    with open(DOCS_DIR / "process_log.md", "a") as f:
        f.write(log_content)
    print("\nProcess log updated.")

    return neighborhood_stats, priority_df


if __name__ == "__main__":
    main()
