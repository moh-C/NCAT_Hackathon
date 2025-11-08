# Challenge 1: Video Stabilization of Microscopic Bacteria

## Overview

Stabilize jittery video of microscopic bacteria using image registration. The solution implements a two-pass alignment approach: sequential frame-to-frame alignment followed by alignment to a golden reference frame.

## Quick Start

### Prerequisites
- Docker installed
- Input TIFF frames in `Challenge1/raw_tiff_frames/` directory

### Running with Docker

1. **Start the container** (from project root):
   ```bash
   docker-compose up -d
   ```

2. **Access Jupyter Lab**:
   - Open `http://localhost:8895` in your browser
   - Get the token from: `docker logs ncat-challenge1`

3. **Run the notebook**:
   - Navigate to `Challenge1/challenge1.ipynb`
   - Run all cells

4. **Stop the container**:
   ```bash
   docker-compose down
   ```

## Solution Method

- **Single-pass**: Sequential alignment of each frame to the previous frame with ROI masking and preprocessing
- **Two-pass**: First pass performs sequential alignment, then all frames are aligned to a golden reference (average of aligned frames) for ultimate precision

## Output

Generates three GIFs: `raw_animation.gif`, `single-stage.gif`, and `two-stage.gif` showing the stabilization results.
