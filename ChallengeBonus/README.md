# Bonus Challenge: 3D Biofilm Visualization Pipeline

## Overview

Develop an alternative to the MATLAB-based biofilmQ → ParaView pipeline that processes 3D microscopy data, computes quantitative biofilm metrics, and generates 3D color-coded visualizations.

## Challenge Requirements

1. Process 3D microscopy data (OME-TIFF)
2. Calculate quantitative metrics like shape_volume
3. Generate 3D color-coded visualizations of biofilms based on calculated metrics

## Solution Approach

The pipeline implements:
- **3D Image Loading**: Reads OME-TIFF files with metadata using `aicsimageio`
- **Segmentation**: Gaussian smoothing + Otsu thresholding + connected component labeling
- **Filtering**: Removes small noisy objects
- **Metrics Calculation**: Computes volume, equivalent diameter, intensity, and other properties in physical units (µm³)
- **Z-axis Interpolation**: Upsamples the Z-axis for smooth 3D meshing
- **3D Visualization**: Creates interactive Plotly visualizations color-coded by metrics

## Quick Start

### Prerequisites
- Docker installed
- OME-TIFF file in `ChallengeBonus/` directory

### Running with Docker

1. **Start the container** (from project root):
   ```bash
   docker-compose up -d
   ```

2. **Access Jupyter Lab**:
   - Open `http://localhost:8895` in your browser
   - Get the token from: `docker logs ncat-challenge1`

3. **Run the notebook**:
   - Navigate to `ChallengeBonus/CB1.ipynb`
   - Update the `FILE_PATH` variable to point to your OME-TIFF file
   - Run all cells

4. **Stop the container**:
   ```bash
   docker-compose down
   ```

## Additional Dependencies

The bonus challenge requires additional packages beyond Challenge1:
- `aicsimageio` - OME-TIFF file reading
- `plotly` - Interactive 3D visualization
- `pandas` - Data analysis and metrics storage

These are automatically installed when building the Docker image. If running locally, install them with:
```bash
pip install aicsimageio plotly pandas
```

## Output

Generates an interactive HTML visualization (`biofilm_visualization.html`) showing 3D biofilm structures color-coded by metrics such as volume, with a colorbar indicating the metric values.

