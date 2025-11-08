# NCAT Hackathon Project

This repository contains solutions for the NCAT Hackathon challenges focused on microscopy image processing and analysis.

## Project Structure

```
NCAT_Hackathon/
├── Challenge1/          # Video stabilization of microscopic bacteria
├── ChallengeBonus/      # 3D biofilm visualization pipeline
├── Dockerfile           # Docker configuration for the project
├── docker-compose.yml   # Docker Compose configuration
└── README.md           # This file
```

## Challenges

### Challenge 1: Video Stabilization
Stabilize jittery video of microscopic bacteria using advanced image registration techniques. Implements both single-pass and two-pass alignment methods for optimal stabilization.

**See [Challenge1/README.md](Challenge1/README.md) for details.**

### Bonus Challenge: 3D Biofilm Visualization
Alternative pipeline to MATLAB-based biofilmQ → ParaView for processing 3D microscopy data. Computes quantitative biofilm metrics and generates interactive 3D color-coded visualizations.

**See [ChallengeBonus/README.md](ChallengeBonus/README.md) for details.**

## Quick Start

### Prerequisites
- Docker installed on your system
- Input data files in respective challenge directories

### Running the Project

1. **Start the Docker container**:
   ```bash
   docker-compose up -d
   ```

2. **Access Jupyter Lab**:
   - Open `http://localhost:8895` in your browser
   - Get the token from: `docker logs ncat-challenge1`

3. **Navigate to the desired challenge**:
   - `Challenge1/challenge1.ipynb` - Video stabilization
   - `ChallengeBonus/CB1.ipynb` - 3D biofilm visualization

4. **Stop the container**:
   ```bash
   docker-compose down
   ```

## Docker Setup

The project uses Docker for consistent environment setup. The container:
- Runs Jupyter Lab on port 8895
- Mounts the project directory for data persistence
- Includes all necessary dependencies for both challenges

## Technologies Used

- **Python 3.11**
- **Jupyter Lab** - Interactive notebook environment
- **scikit-image** - Image processing and analysis
- **numpy/scipy** - Numerical computations
- **matplotlib** - Visualization
- **plotly** - Interactive 3D visualizations (Bonus Challenge)
- **aicsimageio** - OME-TIFF file handling (Bonus Challenge)
- **tifffile** - TIFF image I/O

## About

This project was developed for the NCAT Hackathon, focusing on microscopy image processing challenges including video stabilization and 3D biofilm analysis.
