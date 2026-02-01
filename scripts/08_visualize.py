"""
08_visualize.py
Vegetation-Infrastructure Conflict Prioritization Model
Seattle Area Case Study

This script creates map visualizations:
- Citywide risk map with OpenStreetMap basemap
- Detail map of highest-risk neighborhood
- All neighborhood labels included
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
from pathlib import Path
from datetime import datetime
import contextily as ctx
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# =============================================================================
# Configuration
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
MAPS_DIR = PROJECT_ROOT / "maps"
DOCS_DIR = PROJECT_ROOT / "docs"

# Improved color scheme - higher contrast
RISK_COLORS = {
    'High': '#e31a1c',      # Bright red
    'Medium': '#fec44f',    # Golden yellow
    'Low': '#31a354'        # Forest green
}

# Map styling
FIGURE_DPI = 300
WEB_MERCATOR = "EPSG:3857"

# =============================================================================
# Functions
# =============================================================================

def create_citywide_risk_map(segments: gpd.GeoDataFrame,
                              neighborhoods: gpd.GeoDataFrame,
                              facilities: gpd.GeoDataFrame,
                              save_path: Path) -> plt.Figure:
    """
    Create citywide map with OpenStreetMap basemap and neighborhood labels.
    Focused on Seattle city boundaries.
    """
    print("\nCreating citywide risk map...")

    # Reproject to Web Mercator for basemap compatibility
    print("  Reprojecting to Web Mercator...")
    segments_wm = segments.to_crs(WEB_MERCATOR)
    neighborhoods_wm = neighborhoods.to_crs(WEB_MERCATOR)
    facilities_wm = facilities.to_crs(WEB_MERCATOR)

    # Get Seattle city bounds from neighborhoods (dissolve all neighborhoods)
    seattle_bounds = neighborhoods_wm.total_bounds  # [minx, miny, maxx, maxy]

    # Add small padding (5%) to focus on Seattle
    pad_x = (seattle_bounds[2] - seattle_bounds[0]) * 0.05
    pad_y = (seattle_bounds[3] - seattle_bounds[1]) * 0.05

    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(14, 18))

    # Plot neighborhood boundaries first (subtle)
    neighborhoods_wm.plot(
        ax=ax,
        facecolor='none',
        edgecolor='#444444',
        linewidth=0.8,
        alpha=0.7
    )

    # Plot segments by risk tier (Low first, then Medium, then High)
    print("  Plotting segments by risk tier...")
    for tier in ['Low', 'Medium', 'High']:
        tier_segments = segments_wm[segments_wm['risk_tier'] == tier]
        if len(tier_segments) > 0:
            # Thicker lines for higher risk
            if tier == 'Low':
                linewidth = 0.3
                alpha = 0.5
            elif tier == 'Medium':
                linewidth = 0.6
                alpha = 0.7
            else:  # High
                linewidth = 1.2
                alpha = 0.9

            tier_segments.plot(
                ax=ax,
                color=RISK_COLORS[tier],
                linewidth=linewidth,
                alpha=alpha
            )

    # Plot critical facilities
    hospitals = facilities_wm[facilities_wm['facility_type'] == 'hospital']
    fire_stations = facilities_wm[facilities_wm['facility_type'] == 'fire_station']

    if len(hospitals) > 0:
        hospitals.plot(ax=ax, color='#0571b0', marker='H', markersize=60,
                       zorder=10, alpha=0.9, edgecolor='white', linewidth=0.5)
    if len(fire_stations) > 0:
        fire_stations.plot(ax=ax, color='#ca0020', marker='^', markersize=40,
                           zorder=10, alpha=0.9, edgecolor='white', linewidth=0.5)

    # Add basemap (CartoDB Positron - clean, light style)
    print("  Adding basemap...")
    try:
        ctx.add_basemap(
            ax,
            source=ctx.providers.CartoDB.Positron,
            alpha=0.7,
            attribution_size=6
        )
    except Exception as e:
        print(f"  Warning: Could not add basemap - {e}")

    # Add neighborhood labels
    print("  Adding neighborhood labels...")
    for idx, row in neighborhoods_wm.iterrows():
        if pd.notna(row.get('neighborhood')):
            centroid = row.geometry.centroid
            ax.annotate(
                row['neighborhood'],
                xy=(centroid.x, centroid.y),
                fontsize=5,
                ha='center',
                va='center',
                color='#333333',
                fontweight='bold',
                path_effects=[
                    pe.withStroke(linewidth=2, foreground='white')
                ]
            )

    # Set map bounds to focus on Seattle
    ax.set_xlim(seattle_bounds[0] - pad_x, seattle_bounds[2] + pad_x)
    ax.set_ylim(seattle_bounds[1] - pad_y, seattle_bounds[3] + pad_y)

    # Create legend - position inside the map area (lower left, inside Seattle outline)
    legend_elements = [
        Line2D([0], [0], color=RISK_COLORS['High'], linewidth=3, label='High Risk'),
        Line2D([0], [0], color=RISK_COLORS['Medium'], linewidth=2, label='Medium Risk'),
        Line2D([0], [0], color=RISK_COLORS['Low'], linewidth=1, label='Low Risk'),
        Line2D([0], [0], marker='H', color='w', markerfacecolor='#0571b0',
               markersize=12, label='Hospitals', linestyle='None'),
        Line2D([0], [0], marker='^', color='w', markerfacecolor='#ca0020',
               markersize=10, label='Fire Stations', linestyle='None'),
    ]
    ax.legend(
        handles=legend_elements,
        loc='lower left',
        fontsize=9,
        framealpha=0.95,
        edgecolor='gray',
        fancybox=True,
        bbox_to_anchor=(0.02, 0.02)
    )

    # Title
    ax.set_title(
        'Seattle Area\nVegetation-Infrastructure Conflict Risk Assessment',
        fontsize=18,
        fontweight='bold',
        pad=20
    )

    # Subtitle with statistics
    total_miles = segments['length_ft'].sum() / 5280
    high_risk_miles = segments[segments['risk_tier'] == 'High']['length_ft'].sum() / 5280
    subtitle = f'Total: {total_miles:.0f} miles of overhead lines  |  High Risk: {high_risk_miles:.0f} miles ({high_risk_miles/total_miles*100:.0f}%)'
    ax.text(
        0.5, -0.02,
        subtitle,
        transform=ax.transAxes,
        ha='center',
        fontsize=11,
        color='#555555'
    )

    ax.set_axis_off()
    plt.tight_layout()

    # Save
    print("  Saving map...")
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
    Create detail map of a specific neighborhood with basemap.
    """
    print(f"\nCreating detail map for {neighborhood_name}...")

    # Reproject to Web Mercator
    segments_wm = segments.to_crs(WEB_MERCATOR)
    neighborhoods_wm = neighborhoods.to_crs(WEB_MERCATOR)
    facilities_wm = facilities.to_crs(WEB_MERCATOR)

    # Get the neighborhood boundary
    hood = neighborhoods_wm[neighborhoods_wm['neighborhood'] == neighborhood_name]
    if len(hood) == 0:
        print(f"  Warning: Neighborhood '{neighborhood_name}' not found")
        return None

    hood_geom = hood.geometry.iloc[0]

    # Get bounding box with padding
    minx, miny, maxx, maxy = hood_geom.bounds
    pad_x = (maxx - minx) * 0.15
    pad_y = (maxy - miny) * 0.15
    bounds = (minx - pad_x, miny - pad_y, maxx + pad_x, maxy + pad_y)

    # Filter data within bounds
    segments_bbox = segments_wm.cx[bounds[0]:bounds[2], bounds[1]:bounds[3]]
    facilities_bbox = facilities_wm.cx[bounds[0]:bounds[2], bounds[1]:bounds[3]]

    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(14, 14))

    # Plot nearby neighborhoods for context
    nearby = neighborhoods_wm[neighborhoods_wm['neighborhood'] != neighborhood_name]
    nearby_bbox = nearby.cx[bounds[0]:bounds[2], bounds[1]:bounds[3]]
    nearby_bbox.plot(ax=ax, facecolor='#f0f0f0', edgecolor='#999999',
                     linewidth=0.5, alpha=0.5)

    # Plot target neighborhood boundary
    hood.plot(ax=ax, facecolor='none', edgecolor='#333333', linewidth=2.5)

    # Plot segments by risk tier
    for tier in ['Low', 'Medium', 'High']:
        tier_segments = segments_bbox[segments_bbox['risk_tier'] == tier]
        if len(tier_segments) > 0:
            if tier == 'Low':
                linewidth = 1.0
                alpha = 0.6
            elif tier == 'Medium':
                linewidth = 2.0
                alpha = 0.8
            else:  # High
                linewidth = 3.5
                alpha = 0.95

            tier_segments.plot(
                ax=ax,
                color=RISK_COLORS[tier],
                linewidth=linewidth,
                alpha=alpha
            )

    # Plot facilities
    if len(facilities_bbox) > 0:
        hospitals = facilities_bbox[facilities_bbox['facility_type'] == 'hospital']
        fire_stations = facilities_bbox[facilities_bbox['facility_type'] == 'fire_station']

        if len(hospitals) > 0:
            hospitals.plot(ax=ax, color='#0571b0', marker='H', markersize=150,
                          zorder=10, alpha=0.9, edgecolor='white', linewidth=1)
        if len(fire_stations) > 0:
            fire_stations.plot(ax=ax, color='#ca0020', marker='^', markersize=120,
                              zorder=10, alpha=0.9, edgecolor='white', linewidth=1)

    # Set bounds
    ax.set_xlim(bounds[0], bounds[2])
    ax.set_ylim(bounds[1], bounds[3])

    # Add basemap
    try:
        ctx.add_basemap(
            ax,
            source=ctx.providers.CartoDB.Positron,
            alpha=0.6,
            attribution_size=6
        )
    except Exception as e:
        print(f"  Warning: Could not add basemap - {e}")

    # Legend
    legend_elements = [
        Line2D([0], [0], color=RISK_COLORS['High'], linewidth=4, label='High Risk'),
        Line2D([0], [0], color=RISK_COLORS['Medium'], linewidth=3, label='Medium Risk'),
        Line2D([0], [0], color=RISK_COLORS['Low'], linewidth=2, label='Low Risk'),
    ]

    if len(facilities_bbox) > 0:
        legend_elements.extend([
            Line2D([0], [0], marker='H', color='w', markerfacecolor='#0571b0',
                   markersize=14, label='Hospitals', linestyle='None'),
            Line2D([0], [0], marker='^', color='w', markerfacecolor='#ca0020',
                   markersize=12, label='Fire Stations', linestyle='None'),
        ])

    ax.legend(
        handles=legend_elements,
        loc='upper right',
        fontsize=11,
        framealpha=0.95,
        edgecolor='gray',
        fancybox=True
    )

    # Calculate stats for this neighborhood (use original CRS data)
    hood_orig = neighborhoods[neighborhoods['neighborhood'] == neighborhood_name]
    hood_geom_orig = hood_orig.geometry.iloc[0]
    hood_segments = segments[segments.geometry.centroid.within(hood_geom_orig)]
    total_segs = len(hood_segments)
    high_segs = (hood_segments['risk_tier'] == 'High').sum()
    pct_high = high_segs / total_segs * 100 if total_segs > 0 else 0

    # Title
    ax.set_title(
        f'{neighborhood_name}\n{total_segs:,} segments  |  {high_segs:,} high risk ({pct_high:.0f}%)',
        fontsize=16,
        fontweight='bold',
        pad=15
    )

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
    city_hoods = summary[summary['neighborhood'] != 'Outside City Limits']
    highest_risk = city_hoods.loc[city_hoods['pct_high_risk'].idxmax(), 'neighborhood']
    return highest_risk


def main():
    print("\n" + "="*60)
    print("08_VISUALIZE - Create Improved Map Visualizations")
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

## 08_visualize.py (Improved)
**Run time:** {timestamp}

### Improvements Made
- Added OpenStreetMap basemap (CartoDB Positron)
- Improved color contrast (bright red, golden yellow, forest green)
- Added all neighborhood labels with white halo
- Increased line widths for better visibility
- Larger figure size and improved legend

### Outputs
- `citywide_risk_map.png` - Overview with basemap and labels
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
