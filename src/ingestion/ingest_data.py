import json
import os
import boto3
from botocore.client import Config

def ingest_data_to_minio():
    minio_access_key = os.getenv("MINIO_ROOT_USER", "minio_admin")
    minio_secret_key = os.getenv("MINIO_ROOT_PASSWORD", "minio_password")
    minio_host = "localhost"
    minio_port = "9000"
    minio_endpoint = f"http://{minio_host}:{minio_port}"
    bucket_name = "patient-notes"
    file_path = "data/patient_notes.json"
    object_name = "patient_notes.json"

    s3 = boto3.client(
        "s3",
        endpoint_url=minio_endpoint,
        aws_access_key_id=minio_access_key,
        aws_secret_access_key=minio_secret_key,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1" # MinIO doesn't strictly use regions, but boto3 requires one
    )

    # Create bucket if it doesn't exist
    try:
        s3.head_bucket(Bucket=bucket_name)
    except s3.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            s3.create_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' created.")
        else:
            raise

    # Upload the file
    s3.upload_file(file_path, bucket_name, object_name)
    print(f"Successfully uploaded {file_path} to MinIO bucket '{bucket_name}' as '{object_name}'.")

if __name__ == "__main__":
    ingest_data_to_minio()