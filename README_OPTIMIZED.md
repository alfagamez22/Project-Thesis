# Thesis Prototype - Human Activity Recognition System

## Optimized Setup & Installation

### Prerequisites
- Python 3.8+
- NVIDIA GPU with CUDA support (recommended)
- Anaconda or Miniconda

### Installation Steps

1. **Create and activate conda environment:**
```bash
conda create -n env python=3.10
conda activate env
```

2. **Install PyTorch with CUDA support (for GPU):**
```bash
# For CUDA 11.8
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia

# OR for CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Running the Application

### Method 1: Optimized Startup Script (Recommended)
```bash
python start_server.py
```

### Method 2: Development Mode
```bash
python run_development.py
```

### Method 3: Production Mode (using Waitress)
```bash
python run_production.py
```

### Method 4: Direct app.py (Legacy)
```bash
python app.py
```

## Optimizations Applied

### 1. **Removed WSGI Dependencies**
- Removed `gunicorn` and `eventlet` 
- Using Flask-SocketIO's built-in server for development
- Optional `waitress` for production deployment

### 2. **Suppressed Warnings**
- Fixed `pkg_resources` deprecation warning
- Suppressed `timm` FutureWarnings
- Added proper warning filters in startup code

### 3. **Disabled Auto-Reload**
- Prevents double initialization of GPU models
- Eliminates "Restarting with stat" messages
- Faster startup time

### 4. **GPU Optimization**
- Half-precision (FP16) support for RTX 3060
- Proper CUDA memory management
- Optimized detection frequency

### 5. **Performance Improvements**
- Frame buffering optimization
- Reduced detection frequency (every 6 frames)
- Efficient memory cleanup

## Configuration

### Video Source
Edit `backend/har/livefeed.py` line 49:
```python
# For video file
parser.add_argument("-F", type=str, default="path/to/video.mp4")

# For RTSP stream
parser.add_argument("-F", type=str, default="rtsp://username:password@ip:port/stream")

# For webcam
parser.add_argument("-F", type=str, default=0)
```

### Detection Thresholds
- Person detection: 0.6 (60% confidence)
- Action recognition: 0.23 (23% confidence)
- Detection frequency: Every 6 frames
- Target FPS: 10

### ROI (Region of Interest)
Edit the ROI coordinates in `backend/har/livefeed.py` lines 77-96 to match your camera view.

## API Endpoints

### Video Feed
- `GET /video_feed` - Multipart MJPEG stream
- `GET /video_frame` - Single frame (Safari compatible)

### Activity Recognition
- `GET /activity_status` - Get current AR state
- `POST /toggle_activity` - Toggle AR on/off

### Recording
- `GET /recording_status` - Get recording status
- `POST /toggle_dual_recording` - Start/stop recording
- `GET /list_recordings` - List all recordings
- `GET /recordings/<filename>` - Stream recording
- `DELETE /delete_recording/<filename>` - Delete recording

### Employee Management
- `GET /api/employees` - List all employees
- `POST /api/employees` - Create employee
- `PUT /api/employees/<id>` - Update employee
- `DELETE /api/employees/<id>` - Delete employee

### Activity Monitoring
- `POST /capture_employee_activity` - Manual capture
- `GET /list_employee_captures` - List captures
- `DELETE /clear_employee_captures` - Clear all captures
- `POST /start_employee_monitoring` - Auto-capture (15s interval)
- `POST /stop_employee_monitoring` - Stop auto-capture

### Activity Logs
- `GET /activity_logs` - Get recent activity logs
- `POST /clear_activity_logs` - Clear all logs

## Default Credentials

### User Login
- Username: `username`
- Password: `password`

### Admin Login
- Username: `admin`
- Password: `password`

## Troubleshooting

### WSGI Starting Messages
If you still see "wsgi starting up" messages, ensure:
1. You're not running with gunicorn/eventlet
2. Auto-reload is disabled (`use_reloader=False`)
3. Debug mode is disabled (`debug=False`)

### GPU Not Detected
```bash
# Test GPU
python test_gpu.py

# Verify CUDA installation
python -c "import torch; print(torch.cuda.is_available())"
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use
```bash
# Kill process on port 5000 (Windows)
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

## Performance Tips

1. **Use GPU**: Ensure CUDA is properly installed
2. **Adjust detection frequency**: Increase `-det_freq` for higher FPS
3. **Lower video resolution**: Reduces processing load
4. **Disable unnecessary features**: Turn off recording when not needed

## Project Structure

```
thesis_prototype/
├── app.py                    # Main Flask application
├── start_server.py           # Optimized startup script (NEW)
├── run_development.py        # Development server (NEW)
├── run_production.py         # Production server (NEW)
├── requirements.txt          # Dependencies (OPTIMIZED)
├── backend/
│   ├── har/
│   │   ├── livefeed.py      # Video processing & detection (OPTIMIZED)
│   │   ├── hb/              # Action recognition models (OPTIMIZED)
│   │   └── weights/         # Pre-trained weights
│   ├── postprocess/
│   ├── recordings/
│   └── employee_act/
├── static/
├── templates/
└── user_data.json

## License

Thesis Prototype - Educational Use Only
