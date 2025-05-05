import boto3
import gzip
import io

# Configure Resources for AWS
s3 = boto3.client('s3')
bucket = 'thicc-check-open-food--data' 
key = 'zipped-openfoodfacts-data/openfoodfacts-products.jsonl.gz'
sample_lines_to_extract = 100  
sample_file = 'openfoodfacts-products-sample.jsonl'

# Download only the first N bytes (e.g., 1MB)
N = 1024 * 1024  # 1MB, adjust if needed
print(f"Downloading first {N} bytes from s3://{bucket}/{key} ...")

# Request object in S3
response = s3.get_object(Bucket=bucket, Key=key, Range=f'bytes=0-{N-1}')
compressed_stream = io.BytesIO(response['Body'].read())

print(f"Extracting first {sample_lines_to_extract} lines to {sample_file} ...")
with open(sample_file, 'w') as f:
    with gzip.GzipFile(fileobj=compressed_stream, mode='rb') as gz:
        for i, line in enumerate(gz):
            f.write(line.decode())
            if i + 1 >= sample_lines_to_extract:
                break

print(f"Sample written to {sample_file}") 