"""
Production server for Thesis Prototype
Optimized configuration without WSGI overhead
"""
import os
import sys
import logging
from waitress import serve

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import the Flask app and SocketIO
from app import app, socketio

def run_production_server(host='0.0.0.0', port=5000):
    """
    Run the production server with optimized settings
    """
    logger.info("=" * 60)
    logger.info("Starting Thesis Prototype Production Server")
    logger.info("=" * 60)
    logger.info(f"Server URL: http://{host}:{port}")
    logger.info("Using Waitress WSGI Server (Production)")
    logger.info("=" * 60)
    
    try:
        # Use waitress for production - handles Flask-SocketIO properly
        socketio.run(
            app,
            host=host,
            port=port,
            debug=False,
            use_reloader=False,
            log_output=False  # Let waitress handle logging
        )
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_production_server()
