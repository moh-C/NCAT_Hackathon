# Challenge 1: Video Stabilization of Microscopic Bacteria

## Overview

Challenge 1 focuses on stabilizing jittery video of microscopic bacteria to make them appear perfectly still. The solution uses advanced image registration techniques to align frames and eliminate drift, resulting in a stable, high-quality video output.

## Problem Statement

Given a sequence of segmented TIFF frames containing microscopic bacteria, the goal is to:
1. Load segmented images (30 frames)
2. Stabilize the video by compensating for frame-to-frame drift and jitter
3. Generate stabilized output videos demonstrating the improvement

## Solution Approach

The solution implements a sophisticated two-stage image registration approach:

### Single-Pass Method
- **Sequential Alignment**: Each frame is aligned to the previous frame (not to a static anchor) to handle continuous drift
- **Region of Interest (ROI)**: Focuses alignment on the first 500 columns to avoid interference from bright light bands
- **Preprocessing**: 
  - Contrast stretching (2nd to 98th percentile) to enhance bacteria visibility
  - Gentle Gaussian denoising (σ=0.5) to reduce noise
  - High-pass filtering to emphasize edges for better registration accuracy
- **Sub-pixel Precision**: Uses phase cross-correlation with 50x upsampling for accurate shift detection

### Two-Pass Method (Ultimate Precision)
1. **First Pass**: Performs sequential frame-to-frame alignment (same as single-pass)
2. **Golden Reference Creation**: Averages all aligned frames from the first pass to create a perfect, ultra-clean master image
3. **Second Pass**: Aligns every original frame directly to the golden reference, eliminating cumulative errors from sequential alignment

## Directory Structure

```
Challenge1/
├── README.md                 # This file
├── challenge1.ipynb          # Main Jupyter notebook with implementation
├── requirements.txt          # Python dependencies
├── merge_gifs.py            # Utility script to merge GIFs for comparison
├── raw_tiff_frames/         # Input directory containing frame_*.tif files
├── raw_animation.gif        # Animation of original unstabilized frames
├── single-stage.gif         # Animation after single-pass stabilization
├── two-stage.gif            # Animation after two-pass stabilization
└── merged_gifs.gif          # Side-by-side comparison of all three animations
```

## Dependencies

See `requirements.txt` for the complete list. Key dependencies include:
- `numpy` - Numerical computations
- `matplotlib` - Visualization
- `scikit-image` - Image processing and registration
- `scipy` - Scientific computing
- `tifffile` - TIFF file I/O
- `imageio` - Image I/O and GIF creation
- `jupyterlab` - Jupyter notebook environment

## Setup and Usage

### Prerequisites
- Docker installed on your system
- Input TIFF frames in `Challenge1/raw_tiff_frames/` directory

### Running with Docker

The project uses Docker for consistent environment setup. The Docker container runs Jupyter Lab, allowing you to interact with the notebook.

#### Building the Docker Image

From the project root directory (`NCAT_Hackathon/`):

```bash
docker build -t ncat-hackathon .
```

#### Running the Container with Volume Mounting

**Important**: Volume mounting is required to:
- Persist notebook changes and outputs
- Access input data from the host
- Save generated GIFs and results

##### Option 1: Using Docker Compose (Recommended)

The easiest way to run with proper volume mounting is using Docker Compose:

```bash
docker-compose up -d
```

This will automatically:
- Build the image if needed
- Start the container with volume mounting configured
- Expose port 8895

To stop the container:
```bash
docker-compose down
```

##### Option 2: Using Docker Run

Alternatively, you can run the container directly with volume mounting:

```bash
docker run -d \
  -p 8895:8895 \
  -v $(pwd):/app \
  --name ncat-challenge1 \
  ncat-hackathon
```

Or on Windows PowerShell:
```powershell
docker run -d -p 8895:8895 -v ${PWD}:/app --name ncat-challenge1 ncat-hackathon
```

Or on Windows CMD:
```cmd
docker run -d -p 8895:8895 -v %cd%:/app --name ncat-challenge1 ncat-hackathon
```

#### Accessing Jupyter Lab

Once the container is running:
1. Open your web browser
2. Navigate to `http://localhost:8895`
3. You'll be prompted for a token - get it from the container logs:
   ```bash
   docker logs ncat-challenge1
   ```
4. Look for a line like: `http://127.0.0.1:8895/?token=...`
5. Copy the token and use it to access Jupyter Lab

Alternatively, you can access Jupyter Lab without a token by adding `--NotebookApp.token='' --NotebookApp.password=''` to the CMD in the Dockerfile (not recommended for production).

#### Running the Notebook

1. In Jupyter Lab, navigate to `Challenge1/`
2. Open `challenge1.ipynb`
3. Run all cells sequentially
4. The notebook will:
   - Load frames from `raw_tiff_frames/`
   - Perform single-pass stabilization
   - Perform two-pass stabilization
   - Generate comparison GIFs

#### Stopping the Container

If using Docker Compose:
```bash
docker-compose down
```

If using Docker Run:
```bash
docker stop ncat-challenge1
docker rm ncat-challenge1
```

### Running Locally (Without Docker)

If you prefer to run locally:

```bash
cd Challenge1
pip install -r requirements.txt
jupyter lab
```

Then open `challenge1.ipynb` and run all cells.

## Implementation Details

### Key Functions

- **`preprocess(image)`**: Applies contrast stretching and gentle denoising to enhance features for registration
- **`show_animation(frames, ...)`**: Creates and saves animated GIFs from frame sequences
- **Registration Pipeline**: 
  - Phase cross-correlation for sub-pixel accurate shift detection
  - Cumulative shift tracking for sequential alignment
  - ROI masking to focus on relevant image regions

### Parameters

- **ROI (First Pass)**: First 500 columns (`[:, :500]`)
- **ROI (Second Pass)**: 800x800 region (`[:800, :800]`)
- **Upsampling Factor**: 50x for sub-pixel accuracy
- **Gaussian Filter Sigma**: 0.5 for denoising, 3.0 for high-pass filtering
- **Animation Interval**: 150ms per frame

## Output

The notebook generates three animated GIFs:

1. **`raw_animation.gif`**: Original unstabilized video showing jitter and drift
2. **`single-stage.gif`**: Video after single-pass sequential alignment
3. **`two-stage.gif`**: Video after two-pass alignment with golden reference (best quality)

Additionally, `merge_gifs.py` can be used to create a side-by-side comparison (`merged_gifs.gif`) showing all three animations together.

## Results

The two-pass method achieves excellent stabilization by:
- Eliminating frame-to-frame jitter through sequential alignment
- Removing cumulative errors by aligning to a golden reference
- Maintaining image quality through careful preprocessing
- Focusing on relevant regions using ROI masking

The stabilized output shows bacteria that appear perfectly still, with all drift and jitter eliminated.

## Notes

- The solution handles continuous drift across 30 frames
- Sub-pixel accuracy ensures smooth alignment
- ROI masking prevents interference from artifacts
- Two-pass approach eliminates cumulative errors for ultimate precision

