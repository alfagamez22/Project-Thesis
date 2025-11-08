"""
Optimized startup script for Thesis Prototype
Handles all environment setup and GPU initialization
"""
import os
import sys
import warnings
import logging

# Suppress common warnings before importing heavy libraries
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning, module='pkg_resources')
warnings.filterwarnings('ignore', category=FutureWarning, module='timm')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_gpu():
    """Check GPU availability and print info"""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            logger.info(f"✓ CUDA is available. Found {gpu_count} GPU(s)")
            for i in range(gpu_count):
                gpu_name = torch.cuda.get_device_name(i)
                gpu_memory = torch.cuda.get_device_properties(i).total_memory / (1024**3)
                logger.info(f"  GPU {i}: {gpu_name} ({gpu_memory:.1f} GB)")
            return True
        else:
            logger.warning("⚠ CUDA not available. Using CPU (slower performance)")
            return False
    except Exception as e:
        logger.error(f"Error checking GPU: {e}")
        return False

def main():
    """Main startup function"""
    logger.info("=" * 70)
    logger.info("Starting Thesis Prototype - Human Activity Recognition System")
    logger.info("=" * 70)
    
    # Check GPU
    has_gpu = check_gpu()
    
    # Import and run app
    logger.info("Loading Flask application...")
    from app import app, socketio
    
    logger.info("Initializing video processing...")
    from backend.har import livefeed
    livefeed.start_background_video_thread()
    
    logger.info("=" * 70)
    logger.info("Server Configuration:")
    logger.info("  URL: http://0.0.0.0:5000")
    logger.info("  GPU Acceleration: " + ("Enabled" if has_gpu else "Disabled"))
    logger.info("  Auto-reload: Disabled (prevents GPU reinitialization)")
    logger.info("  Debug Mode: Disabled (production-ready)")
    logger.info("=" * 70)
    logger.info("Press Ctrl+C to stop the server")
    logger.info("=" * 70)
    
    try:
        # Run with optimized settings
        socketio.run(
            app,
            host="0.0.0.0",
            port=5000,
            debug=False,
            use_reloader=False,
            log_output=True,
            allow_unsafe_werkzeug=True
        )
    except KeyboardInterrupt:
        logger.info("\n" + "=" * 70)
        logger.info("Server shutdown requested")
        logger.info("=" * 70)
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
