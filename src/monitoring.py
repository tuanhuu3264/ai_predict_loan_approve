import logging
import json
from datetime import datetime
import boto3
from prometheus_client import start_http_server, Counter, Histogram
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Prometheus metrics
PREDICTION_COUNTER = Counter('model_predictions_total', 'Total number of predictions made')
PREDICTION_LATENCY = Histogram('prediction_latency_seconds', 'Time spent processing prediction')
ERROR_COUNTER = Counter('model_errors_total', 'Total number of prediction errors')

class ModelMonitor:
    def __init__(self, model_name="loan_scoring_model"):
        self.model_name = model_name
        self.s3_client = boto3.client('s3')
        self.cloudwatch = boto3.client('cloudwatch')
        
    def log_prediction(self, prediction, features, actual=None):
        """Log prediction results and metrics"""
        try:
            # Log to CloudWatch
            self.cloudwatch.put_metric_data(
                Namespace='LoanScoring',
                MetricData=[
                    {
                        'MetricName': 'PredictionScore',
                        'Value': float(prediction),
                        'Unit': 'None',
                        'Timestamp': datetime.utcnow()
                    }
                ]
            )
            
            # Log prediction details
            log_entry = {
                'timestamp': datetime.utcnow().isoformat(),
                'prediction': float(prediction),
                'features': features,
                'actual': actual
            }
            
            # Save to S3 for later analysis
            self.s3_client.put_object(
                Bucket='hackathon-s322',
                Key=f'predictions/{datetime.utcnow().strftime("%Y/%m/%d")}/prediction_{datetime.utcnow().timestamp()}.json',
                Body=json.dumps(log_entry)
            )
            
            PREDICTION_COUNTER.inc()
            
        except Exception as e:
            logger.error(f"Error logging prediction: {str(e)}")
            ERROR_COUNTER.inc()
    
    def log_error(self, error_message):
        """Log model errors"""
        logger.error(error_message)
        ERROR_COUNTER.inc()
        
        self.cloudwatch.put_metric_data(
            Namespace='LoanScoring',
            MetricData=[
                {
                    'MetricName': 'ModelErrors',
                    'Value': 1,
                    'Unit': 'Count',
                    'Timestamp': datetime.utcnow()
                }
            ]
        )

def start_monitoring_server(port=8000):
    """Start Prometheus metrics server"""
    start_http_server(port)
    logger.info(f"Monitoring server started on port {port}")

if __name__ == "__main__":
    # Start monitoring server
    start_monitoring_server()
    
    # Example usage
    monitor = ModelMonitor()
    
    # Keep the script running
    while True:
        time.sleep(1) 