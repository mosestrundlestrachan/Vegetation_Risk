"""
06_risk_scoring.py
Vegetation-Infrastructure Conflict Prioritization Model
Seattle City Light Portfolio Project

This script calculates composite risk scores:
- Normalizes each factor to 0-1 scale
- Applies weighted scoring:
  - Vegetation load: 50%
  - Critical facility proximity: 30%
  - Segment length: 20%
- Classifies into risk tiers: High (top 20%), Medium (middle 40%), Low (bottom 40%)
"""

import geopandas as gpd
import numpy as np
from pathlib import Path
from datetime import datetime

# =============================================================================
# Configuration
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DOCS_DIR = PROJECT_ROOT / "docs"

# Risk scoring weights
WEIGHTS = {
    'vegetation': 0.50,   # 50% - vegetation load
    'proximity': 0.30,    # 30% - critical facility proximity
    'length': 0.20        # 20% - segment length
}

# Risk tier percentiles
TIER_THRESHOLDS = {
    'high': 80,    # Top 20% = High risk
    'medium': 40   # Middle 40% = Medium risk, Bottom 40% = Low risk
}

# =============================================================================
# Functions
# =============================================================================

def normalize_min_max(series):
    """
    Normalize a series to 0-1 scale using min-max normalization.
    Handles edge case where all values are the same.
    """
    min_val = series.min()
    max_val = series.max()

    if max_val == min_val:
        return np.zeros(len(series))

    return (series - min_val) / (max_val - min_val)


def classify_risk_tier(score, high_threshold, medium_threshold):
    """Classify risk score into tier."""
    if score >= high_threshold:
        return 'High'
    elif score >= medium_threshold:
        return 'Medium'
    else:
        return 'Low'


def main():
    print("\n" + "="*60)
    print("06_RISK_SCORING - Calculate Composite Risk Scores")
    print("="*60)

    # Load data with all metrics
    print("\nLoading data...")
    lines_path = PROCESSED_DIR / "lines_with_proximity.gpkg"
    lines = gpd.read_file(lines_path)
    print(f"  Loaded {len(lines):,} line segments")

    # Verify required columns exist
    required_cols = ['canopy_sqft_per_ft', 'proximity_score', 'length_ft']
    for col in required_cols:
        if col not in lines.columns:
            raise ValueError(f"Missing required column: {col}")
    print(f"  Required columns verified: {required_cols}")

    # ==========================================================================
    # Step 1: Normalize each factor to 0-1 scale
    # ==========================================================================
    print("\nNormalizing risk factors...")

    # Vegetation load (canopy per linear foot) - higher = more risk
    lines['veg_norm'] = normalize_min_max(lines['canopy_sqft_per_ft'])
    print(f"  Vegetation: min={lines['veg_norm'].min():.3f}, max={lines['veg_norm'].max():.3f}")

    # Proximity score (3/2/1) - already scored, just normalize to 0-1
    # Score 3 = highest priority, normalize so 3 -> 1.0, 1 -> 0.33
    lines['prox_norm'] = lines['proximity_score'] / 3
    print(f"  Proximity: min={lines['prox_norm'].min():.3f}, max={lines['prox_norm'].max():.3f}")

    # Segment length - longer = more exposure = higher risk
    lines['length_norm'] = normalize_min_max(lines['length_ft'])
    print(f"  Length: min={lines['length_norm'].min():.3f}, max={lines['length_norm'].max():.3f}")

    # ==========================================================================
    # Step 2: Calculate weighted composite risk score
    # ==========================================================================
    print("\nCalculating composite risk scores...")
    print(f"  Weights: Vegetation={WEIGHTS['vegetation']:.0%}, "
          f"Proximity={WEIGHTS['proximity']:.0%}, Length={WEIGHTS['length']:.0%}")

    lines['risk_score'] = (
        lines['veg_norm'] * WEIGHTS['vegetation'] +
        lines['prox_norm'] * WEIGHTS['proximity'] +
        lines['length_norm'] * WEIGHTS['length']
    )

    # ==========================================================================
    # Step 3: Classify into risk tiers
    # ==========================================================================
    print("\nClassifying risk tiers...")

    # Calculate percentile thresholds
    high_threshold = np.percentile(lines['risk_score'], TIER_THRESHOLDS['high'])
    medium_threshold = np.percentile(lines['risk_score'], TIER_THRESHOLDS['medium'])

    print(f"  High threshold (P{TIER_THRESHOLDS['high']}): {high_threshold:.4f}")
    print(f"  Medium threshold (P{TIER_THRESHOLDS['medium']}): {medium_threshold:.4f}")

    # Apply classification
    lines['risk_tier'] = lines['risk_score'].apply(
        lambda x: classify_risk_tier(x, high_threshold, medium_threshold)
    )

    # ==========================================================================
    # Step 4: Create priority ranking
    # ==========================================================================
    print("\nCreating priority ranking...")
    lines['priority_rank'] = lines['risk_score'].rank(ascending=False, method='first').astype(int)

    # ==========================================================================
    # Export results
    # ==========================================================================
    print("\nExporting results...")
    output_path = PROCESSED_DIR / "scored_segments.gpkg"
    lines.to_file(output_path, driver="GPKG")
    print(f"  Saved: {output_path}")

    # ==========================================================================
    # Summary statistics
    # ==========================================================================
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    tier_counts = lines['risk_tier'].value_counts()
    tier_lengths = lines.groupby('risk_tier')['length_ft'].sum() / 5280  # Convert to miles

    print(f"\n  Risk Score Statistics:")
    print(f"    Mean: {lines['risk_score'].mean():.4f}")
    print(f"    Median: {lines['risk_score'].median():.4f}")
    print(f"    Std Dev: {lines['risk_score'].std():.4f}")
    print(f"    Min: {lines['risk_score'].min():.4f}")
    print(f"    Max: {lines['risk_score'].max():.4f}")

    print(f"\n  Risk Tier Distribution:")
    for tier in ['High', 'Medium', 'Low']:
        count = tier_counts.get(tier, 0)
        miles = tier_lengths.get(tier, 0)
        pct = count / len(lines) * 100
        print(f"    {tier:8}: {count:,} segments ({pct:5.1f}%) - {miles:.1f} miles")

    print(f"\n  Top 10 Highest Risk Segments:")
    top10 = lines.nsmallest(10, 'priority_rank')[
        ['segment_id', 'risk_score', 'risk_tier', 'canopy_sqft_per_ft',
         'proximity_score', 'length_ft']
    ]
    print(top10.to_string(index=False))

    # Update process log
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_content = f"""
---

## 06_risk_scoring.py
**Run time:** {timestamp}

### Actions
- Normalized all risk factors to 0-1 scale
- Applied weighted scoring: Vegetation {WEIGHTS['vegetation']:.0%}, Proximity {WEIGHTS['proximity']:.0%}, Length {WEIGHTS['length']:.0%}
- Classified into risk tiers based on percentiles

### Risk Score Statistics
| Metric | Value |
|--------|-------|
| Mean | {lines['risk_score'].mean():.4f} |
| Median | {lines['risk_score'].median():.4f} |
| Std Dev | {lines['risk_score'].std():.4f} |
| Min | {lines['risk_score'].min():.4f} |
| Max | {lines['risk_score'].max():.4f} |

### Risk Tier Distribution
| Tier | Segments | Percentage | Miles |
|------|----------|------------|-------|
| High | {tier_counts.get('High', 0):,} | {tier_counts.get('High', 0)/len(lines)*100:.1f}% | {tier_lengths.get('High', 0):.1f} |
| Medium | {tier_counts.get('Medium', 0):,} | {tier_counts.get('Medium', 0)/len(lines)*100:.1f}% | {tier_lengths.get('Medium', 0):.1f} |
| Low | {tier_counts.get('Low', 0):,} | {tier_counts.get('Low', 0)/len(lines)*100:.1f}% | {tier_lengths.get('Low', 0):.1f} |

Output: `scored_segments.gpkg`

"""
    with open(DOCS_DIR / "process_log.md", "a") as f:
        f.write(log_content)
    print("\nProcess log updated.")

    return lines


if __name__ == "__main__":
    main()
