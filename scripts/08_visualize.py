"""
08_visualize.py
Vegetation-Infrastructure Conflict Prioritization Model
Seattle City Light Portfolio Project

This script creates map visualizations:
- Citywide risk map colored by risk tier (matplotlib)
- Detail map of highest-risk neighborhood
- Saves to /maps folder
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from pathlib import Path
from datetime import datetime

# =============================================================================
# Configuration
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
MAPS_DIR = PROJECT_ROOT / "maps"
DOCS_DIR = PROJECT_ROOT / "docs"

# Color scheme for risk tiers
RISK_COLORS = {
    'High': '#d62728',      # Red
    'Medium': '#ff7f0e',    # Orange
    'Low': '#2ca02c'        # Green
}

# Map styling
FIGURE_DPI = 300
BACKGROUND_COLOR = '#f5f5f5'

# =============================================================================
# Functions
# =============================================================================

def create_citywide_risk_map(segments: gpd.GeoDataFrame,
                              neighborhoods: gpd.GeoDataFrame,
                              facilities: gpd.GeoDataFrame,
                              save_path: Path) -> plt.Figure:
    """
    Create citywide map showing all line segments colored by risk tier.
    """
    print("\nCreating citywide risk map...")

    fig, ax = plt.subplots(1, 1, figsize=(14, 16))
    ax.set_facecolor(BACKGROUND_COLOR)

    # Plot neighborhood boundaries as context
    neighborhoods.plot(
        ax=ax,
        facecolor='white',
        edgecolor='gray',
        linewidth=0.3,
        alpha=0.5
    )

    # Plot segments by risk tier (Low first, then Medium, then High so High is on top)
    for tier in ['Low', 'Medium', 'High']:
        tier_segments = segments[segments['risk_tier'] == tier]
        if len(tier_segments) > 0:
            linewidth = 0.5 if tier == 'Low' else 0.8 if tier == 'Medium' else 1.2
            tier_segments.plot(
                ax=ax,
                color=RISK_COLORS[tier],
                linewidth=linewidth,
                alpha=0.7
            )

    # Plot critical facilities
    hospitals = facilities[facilities['facility_type'] == 'hospital']
    fire_stations = facilities[facilities['facility_type'] == 'fire_station']

    hospitals.plot(ax=ax, color='blue', marker='s', markersize=30,
                   label='Hospitals', zorder=5, alpha=0.8)
    fire_stations.plot(ax=ax, color='darkred', marker='^', markersize=25,
                       label='Fire Stations', zorder=5, alpha=0.8)

    # Create legend
    legend_elements = [
        Line2D([0], [0], color=RISK_COLORS['High'], linewidth=2, label='High Risk'),
        Line2D([0], [0], color=RISK_COLORS['Medium'], linewidth=2, label='Medium Risk'),
        Line2D([0], [0], color=RISK_COLORS['Low'], linewidth=2, label='Low Risk'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='blue',
               markersize=10, label='Hospitals'),
        Line2D([0], [0], marker='^', color='w', markerfacecolor='darkred',
               markersize=10, label='Fire Stations'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10,
              framealpha=0.9, edgecolor='gray')

    # Titles and labels
    ax.set_title('Seattle City Light\nVegetation-Infrastructure Conflict Risk Assessment',
                fontsize=16, fontweight='bold', pad=20)

    # Add subtitle with statistics
    total_miles = segments['length_ft'].sum() / 5280
    high_risk_miles = segments[segments['risk_tier'] == 'High']['length_ft'].sum() / 5280
    subtitle = f'Total: {total_miles:.0f} miles of overhead lines | High Risk: {high_risk_miles:.0f} miles ({high_risk_miles/total_miles*100:.0f}%)'
    ax.text(0.5, -0.02, subtitle, transform=ax.transAxes, ha='center',
            fontsize=10, color='gray')

    ax.set_axis_off()
    plt.tight_layout()

    # Save
    fig.savefig(save_path, dpi=FIGURE_DPI, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"  Saved: {save_path}")

    return fig


def create_detail_map(segments: gpd.GeoDataFrame,
                      neighborhoods: gpd.GeoDataFrame,
                      facilities: gpd.GeoDataFrame,
                      neighborhood_name: str,
                      save_path: Path) -> plt.Figure:
    """
    Create detail map of a specific high-risk neighborhood.
    """
    print(f"\nCreating detail map for {neighborhood_name}...")

    # Get the neighborhood boundary
    hood = neighborhoods[neighborhoods['neighborhood'] == neighborhood_name]
    if len(hood) == 0:
        print(f"  Warning: Neighborhood '{neighborhood_name}' not found")
        return None

    hood_geom = hood.geometry.iloc[0]

    # Get bounding box with padding
    minx, miny, maxx, maxy = hood_geom.bounds
    pad = (maxx - minx) * 0.1  # 10% padding
    bounds = (minx - pad, miny - pad, maxx + pad, maxy + pad)

    # Filter segments within bounds
    segments_bbox = segments.cx[bounds[0]:bounds[2], bounds[1]:bounds[3]]

    # Filter facilities within bounds
    facilities_bbox = facilities.cx[bounds[0]:bounds[2], bounds[1]:bounds[3]]

    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    ax.set_facecolor(BACKGROUND_COLOR)

    # Plot neighborhood boundary
    hood.plot(ax=ax, facecolor='white', edgecolor='black', linewidth=2)

    # Plot nearby neighborhoods for context
    nearby = neighborhoods[neighborhoods['neighborhood'] != neighborhood_name]
    nearby_bbox = nearby.cx[bounds[0]:bounds[2], bounds[1]:bounds[3]]
    nearby_bbox.plot(ax=ax, facecolor='#e8e8e8', edgecolor='gray',
                     linewidth=0.5, alpha=0.5)

    # Plot segments by risk tier
    for tier in ['Low', 'Medium', 'High']:
        tier_segments = segments_bbox[segments_bbox['risk_tier'] == tier]
        if len(tier_segments) > 0:
            linewidth = 1.0 if tier == 'Low' else 1.5 if tier == 'Medium' else 2.5
            tier_segments.plot(
                ax=ax,
                color=RISK_COLORS[tier],
                linewidth=linewidth,
                alpha=0.8
            )

    # Plot facilities
    if len(facilities_bbox) > 0:
        hospitals = facilities_bbox[facilities_bbox['facility_type'] == 'hospital']
        fire_stations = facilities_bbox[facilities_bbox['facility_type'] == 'fire_station']

        if len(hospitals) > 0:
            hospitals.plot(ax=ax, color='blue', marker='s', markersize=80,
                          zorder=5, alpha=0.9)
        if len(fire_stations) > 0:
            fire_stations.plot(ax=ax, color='darkred', marker='^', markersize=60,
                              zorder=5, alpha=0.9)

    # Set bounds
    ax.set_xlim(bounds[0], bounds[2])
    ax.set_ylim(bounds[1], bounds[3])

    # Legend
    legend_elements = [
        Line2D([0], [0], color=RISK_COLORS['High'], linewidth=3, label='High Risk'),
        Line2D([0], [0], color=RISK_COLORS['Medium'], linewidth=2, label='Medium Risk'),
        Line2D([0], [0], color=RISK_COLORS['Low'], linewidth=1, label='Low Risk'),
    ]

    if len(facilities_bbox) > 0:
        legend_elements.extend([
            Line2D([0], [0], marker='s', color='w', markerfacecolor='blue',
                   markersize=10, label='Hospitals'),
            Line2D([0], [0], marker='^', color='w', markerfacecolor='darkred',
                   markersize=10, label='Fire Stations'),
        ])

    ax.legend(handles=legend_elements, loc='upper right', fontsize=10,
              framealpha=0.9, edgecolor='gray')

    # Calculate stats for this neighborhood
    hood_segments = segments[segments.geometry.centroid.within(hood_geom)]
    total_segs = len(hood_segments)
    high_segs = (hood_segments['risk_tier'] == 'High').sum()
    pct_high = high_segs / total_segs * 100 if total_segs > 0 else 0

    # Title
    ax.set_title(f'{neighborhood_name} - Detail View\n'
                f'{total_segs:,} segments | {high_segs:,} high risk ({pct_high:.0f}%)',
                fontsize=14, fontweight='bold', pad=15)

    ax.set_axis_off()
    plt.tight_layout()

    # Save
    fig.savefig(save_path, dpi=FIGURE_DPI, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"  Saved: {save_path}")

    return fig


def find_highest_risk_neighborhood(neighborhood_summary_path: Path) -> str:
    """Find the neighborhood with highest risk percentage."""
    summary = pd.read_csv(neighborhood_summary_path)

    # Filter out "Outside City Limits" and find highest risk
    city_hoods = summary[summary['neighborhood'] != 'Outside City Limits']
    highest_risk = city_hoods.loc[city_hoods['pct_high_risk'].idxmax(), 'neighborhood']

    return highest_risk


def main():
    print("\n" + "="*60)
    print("08_VISUALIZE - Create Map Visualizations")
    print("="*60)

    # Ensure output directory exists
    MAPS_DIR.mkdir(parents=True, exist_ok=True)

    # Load data
    print("\nLoading data...")
    segments = gpd.read_file(PROCESSED_DIR / "scored_segments.gpkg")
    neighborhoods = gpd.read_file(PROCESSED_DIR / "neighborhoods.gpkg")
    facilities = gpd.read_file(PROCESSED_DIR / "critical_facilities.gpkg")

    print(f"  Loaded {len(segments):,} scored segments")
    print(f"  Loaded {len(neighborhoods):,} neighborhoods")
    print(f"  Loaded {len(facilities):,} critical facilities")

    # ==========================================================================
    # Map 1: Citywide Risk Map
    # ==========================================================================
    citywide_path = MAPS_DIR / "citywide_risk_map.png"
    create_citywide_risk_map(segments, neighborhoods, facilities, citywide_path)

    # ==========================================================================
    # Map 2: Detail Map of Highest-Risk Neighborhood
    # ==========================================================================
    # Find highest risk neighborhood
    highest_risk_hood = find_highest_risk_neighborhood(
        OUTPUTS_DIR / "neighborhood_summary.csv"
    )
    print(f"\n  Highest risk neighborhood: {highest_risk_hood}")

    detail_path = MAPS_DIR / "detail_high_risk_area.png"
    create_detail_map(segments, neighborhoods, facilities, highest_risk_hood, detail_path)

    # ==========================================================================
    # Summary
    # ==========================================================================
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"\n  Maps created:")
    print(f"    1. {citywide_path}")
    print(f"    2. {detail_path}")

    # Update process log
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_content = f"""
---

## 08_visualize.py
**Run time:** {timestamp}

### Actions
- Created citywide risk map (all segments colored by tier)
- Created detail map of highest-risk neighborhood ({highest_risk_hood})

### Outputs
- `citywide_risk_map.png` - Overview of all Seattle area
- `detail_high_risk_area.png` - Zoomed view of {highest_risk_hood}

"""
    with open(DOCS_DIR / "process_log.md", "a") as f:
        f.write(log_content)
    print("\nProcess log updated.")

    # Close figures to free memory
    plt.close('all')

    print("\nVisualization complete!")


if __name__ == "__main__":
    main()
