import os
import shutil
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def cleanup_old_artifacts(days_to_keep=7):
    """
    Clean up old model artifacts and temporary files
    Args:
        days_to_keep (int): Number of days to keep artifacts
    """
    try:
        # Clean up old model versions
        model_dir = "model"
        if os.path.exists(model_dir):
            current_time = datetime.now()
            for item in os.listdir(model_dir):
                item_path = os.path.join(model_dir, item)
                if os.path.isfile(item_path):
                    file_time = datetime.fromtimestamp(os.path.getctime(item_path))
                    if current_time - file_time > timedelta(days=days_to_keep):
                        os.remove(item_path)
                        logger.info(f"Removed old model file: {item_path}")

        # Clean up temporary files
        temp_dirs = ["tmp", "temp", "__pycache__"]
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                logger.info(f"Removed temporary directory: {temp_dir}")

        # Clean up old logs
        log_dir = "logs"
        if os.path.exists(log_dir):
            current_time = datetime.now()
            for log_file in os.listdir(log_dir):
                if log_file.endswith(".log"):
                    log_path = os.path.join(log_dir, log_file)
                    file_time = datetime.fromtimestamp(os.path.getctime(log_path))
                    if current_time - file_time > timedelta(days=days_to_keep):
                        os.remove(log_path)
                        logger.info(f"Removed old log file: {log_path}")

        # Clean up old predictions
        pred_dir = "predictions"
        if os.path.exists(pred_dir):
            current_time = datetime.now()
            for pred_file in os.listdir(pred_dir):
                if pred_file.endswith(".json"):
                    pred_path = os.path.join(pred_dir, pred_file)
                    file_time = datetime.fromtimestamp(os.path.getctime(pred_path))
                    if current_time - file_time > timedelta(days=days_to_keep):
                        os.remove(pred_path)
                        logger.info(f"Removed old prediction file: {pred_path}")

        logger.info("Cleanup completed successfully")
        
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
        raise

if __name__ == "__main__":
    cleanup_old_artifacts() 