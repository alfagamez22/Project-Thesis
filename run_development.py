"""
Development server for Thesis Prototype
Optimized for development with auto-reload disabled to prevent GPU reinitialization
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import the Flask app and SocketIO
from app import app, socketio

def run_development_server(host='0.0.0.0', port=5000):
    """
    Run the development server with optimized settings
    """
    logger.info("=" * 60)
    logger.info("Starting Thesis Prototype Development Server")
    logger.info("=" * 60)
    logger.info(f"Server URL: http://{host}:{port}")
    logger.info("Auto-reload: DISABLED (prevents GPU reinitialization)")
    logger.info("=" * 60)
    
    try:
        # Run with Flask-SocketIO's built-in server
        socketio.run(
            app,
            host=host,
            port=port,
            debug=False,  # Disable debug to prevent double loading
            use_reloader=False,  # Disable reloader to prevent GPU reinitialization
            log_output=True,
            allow_unsafe_werkzeug=True
        )
    except KeyboardInterrupt:
        logger.info("\nServer shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_development_server()
