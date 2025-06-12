import os
import boto3
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ModelArtifactManager:
    def __init__(self, bucket_name='hackathon-s322'):
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name
        
    def upload_model_artifacts(self, model_dir='model'):
        """Upload model artifacts to S3"""
        try:
            # Create timestamp for versioning
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            
            # List of files to upload
            files_to_upload = [
                'xgb_model.json',
                'ohe.pkl',
                'scaler.pkl',
                'feature_cols.pkl'
            ]
            
            # Upload each file
            for file_name in files_to_upload:
                local_path = os.path.join(model_dir, file_name)
                if os.path.exists(local_path):
                    s3_key = f'models/{timestamp}/{file_name}'
                    self.s3_client.upload_file(
                        local_path,
                        self.bucket_name,
                        s3_key
                    )
                    logger.info(f"Uploaded {file_name} to s3://{self.bucket_name}/{s3_key}")
                else:
                    logger.warning(f"File not found: {local_path}")
            
            # Create metadata file
            metadata = {
                'timestamp': timestamp,
                'model_version': timestamp,
                'files': files_to_upload,
                'upload_time': datetime.utcnow().isoformat()
            }
            
            # Upload metadata
            metadata_key = f'models/{timestamp}/metadata.json'
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=metadata_key,
                Body=json.dumps(metadata, indent=2)
            )
            logger.info(f"Uploaded metadata to s3://{self.bucket_name}/{metadata_key}")
            
            return timestamp
            
        except Exception as e:
            logger.error(f"Error uploading model artifacts: {str(e)}")
            raise
    
    def download_latest_model(self, model_dir='model'):
        """Download the latest model artifacts from S3"""
        try:
            # List all model versions
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix='models/'
            )
            
            # Get the latest version
            versions = [obj['Key'].split('/')[1] for obj in response.get('Contents', []) 
                       if obj['Key'].endswith('metadata.json')]
            if not versions:
                raise ValueError("No model versions found in S3")
            
            latest_version = sorted(versions)[-1]
            
            # Download each file
            files_to_download = [
                'xgb_model.json',
                'ohe.pkl',
                'scaler.pkl',
                'feature_cols.pkl'
            ]
            
            os.makedirs(model_dir, exist_ok=True)
            
            for file_name in files_to_download:
                s3_key = f'models/{latest_version}/{file_name}'
                local_path = os.path.join(model_dir, file_name)
                self.s3_client.download_file(
                    self.bucket_name,
                    s3_key,
                    local_path
                )
                logger.info(f"Downloaded {file_name} from s3://{self.bucket_name}/{s3_key}")
            
            return latest_version
            
        except Exception as e:
            logger.error(f"Error downloading model artifacts: {str(e)}")
            raise

if __name__ == "__main__":
    # Example usage
    manager = ModelArtifactManager()
    
    # Upload model artifacts
    version = manager.upload_model_artifacts()
    print(f"Uploaded model version: {version}")
    
    # Download latest model
    latest = manager.download_latest_model()
    print(f"Downloaded model version: {latest}") 