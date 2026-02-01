# Methodology
## Vegetation-Infrastructure Conflict Prioritization Model

### Overview

This document describes the methodology used to identify and prioritize overhead power line segments at risk of vegetation-related outages for Seattle City Light.

---

## Data Sources

| Dataset | Description | Source |
|---------|-------------|--------|
| Seattle Tree Canopy 2021 | LiDAR-derived canopy polygons | Seattle GIS Open Data |
| Seattle City Light Lines | Power line network (OH/UG) | Seattle City Light |
| Seattle City Light Poles | Utility pole locations | Seattle City Light |
| Fire Stations | Critical facility points | Seattle GIS Open Data |
| Hospitals | Critical facility points | Seattle GIS Open Data |
| Neighborhoods | Boundary polygons | Seattle GIS Open Data |

All datasets use NAD83 State Plane Washington North (US Feet) coordinate system.

---

## Risk Scoring Model

### Factor 1: Vegetation Load (50% weight)

**Metric:** Canopy square feet per linear foot of line

**Methodology:**
1. Create 15-foot buffer around each overhead line segment
2. Intersect buffer with tree canopy polygons
3. Calculate total canopy area within buffer
4. Normalize by segment length: `canopy_area / segment_length`

**Rationale:** Higher vegetation density near power lines increases probability of tree-related contact during storms or growth periods.

### Factor 2: Critical Facility Proximity (30% weight)

**Metric:** Distance score based on proximity to hospitals and fire stations

**Scoring:**
| Distance | Score | Priority |
|----------|-------|----------|
| < 500 ft | 3 | High |
| 500-1500 ft | 2 | Medium |
| > 1500 ft | 1 | Low |

**Methodology:**
1. Calculate centroid of each line segment
2. Find distance to nearest critical facility (hospital or fire station)
3. Classify into proximity score

**Rationale:** Power outages near critical facilities have greater public safety impact.

### Factor 3: Segment Length (20% weight)

**Metric:** Total linear feet of segment

**Methodology:**
1. Calculate geometry length of each segment
2. Normalize using min-max scaling to 0-1 range

**Rationale:** Longer segments have more potential points of vegetation contact.

### Composite Risk Score

```
risk_score = (veg_norm × 0.50) + (prox_norm × 0.30) + (length_norm × 0.20)
```

Where all factors are normalized to 0-1 scale.

### Risk Tier Classification

| Tier | Percentile | Description |
|------|------------|-------------|
| High | Top 20% | Immediate attention required |
| Medium | Middle 40% | Include in regular maintenance |
| Low | Bottom 40% | Monitor during routine patrols |

---

## Assumptions and Limitations

### Assumptions

1. **15-foot buffer approximation**: The clearance zone is approximated at 15 feet for all distribution lines. Actual required clearance varies by voltage level and local regulations.

2. **Canopy as proxy for risk**: Tree canopy presence indicates potential for vegetation-infrastructure conflict. This does not account for:
   - Species-specific growth rates
   - Tree health or stability
   - Recent trimming activity

3. **Uniform facility weighting**: All hospitals and fire stations are weighted equally regardless of size or service area.

### Limitations

1. **No historical outage data**: This model is predictive only and has not been validated against historical vegetation-caused outages.

2. **Static canopy data**: Tree canopy data from 2021 may not reflect current conditions.

3. **Buffer simplification**: A uniform buffer width does not account for wire sag, span length, or conductor configuration.

4. **Critical facility scope**: Only hospitals and fire stations are included. Other critical infrastructure (water treatment, communications, etc.) is not considered.

---

## Recommended Use

This model is intended to:
- Prioritize inspection routes for vegetation management crews
- Identify areas for proactive trimming programs
- Support capital planning for system hardening

This model should **not** be used as:
- The sole basis for emergency response
- A replacement for field inspection
- A guarantee of outage prevention

---

## Future Enhancements

Potential improvements for future iterations:

1. **Validation with historical data**: Calibrate weights using actual outage records
2. **Species-specific risk**: Incorporate tree species data where available
3. **Dynamic weather overlays**: Weight risk by local wind exposure
4. **Customer impact scoring**: Weight by downstream customer count
5. **Maintenance history integration**: Account for recent trimming activities
