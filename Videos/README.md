# Videos - Demo & Tutorials

## 📹 Contents

This folder contains demonstration videos for the AVOSDIM Factory Planning System:

### 1. `Simulation_in_witness.mp4`
- **Duration**: Demo video
- **Content**: Simulation demonstration using Witness software
- **Topics**: Visual simulation of production planning results

### 2. `Optimization.mp4`
- **Duration**: Tutorial video
- **Content**: Optimization module demonstration
- **Topics**: Running optimization, interpreting results, Pareto front analysis

## Viewing Options

### Web Browser
```bash
# Clone repository and navigate to Videos folder
cd Videos
# Open .mp4 files with any video player
```

### From Streamlit Interface
The interface can be extended to display embedded videos:

```python
import streamlit as st

st.video('Videos/Optimization.mp4')
```

## System Requirements

- Video player: VLC, Windows Media Player, or any modern browser
- Disk space: ~500MB for both videos
- Internet: Not required (local files)

## Troubleshooting

**Video won't play:**
- Ensure codec support (H.264 recommended)
- Try different video player
- Check file integrity

**Can't download videos:**
- Use Git LFS (Large File Storage) for better management
- Videos are included in repository by default

## Contributing

To add new demonstration videos:
1. Record at 1080p, 30fps minimum
2. Export as MP4 with H.264 codec
3. Keep file size under 500MB
4. Add description in this README

---

**Note**: These videos are included for reference. The system operates independently through the command line and Streamlit interface.
