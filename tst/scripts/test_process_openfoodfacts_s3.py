import unittest
from unittest.mock import patch, MagicMock
import io
import gzip
import json
import os
import sys

# Add src/scripts to the path for import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/scripts')))
from process_openfoodfacts_s3 import extractFields, process_s3_jsonl_batches_to_s3

class TestProcessOpenfoodfactsS3(unittest.TestCase):
    @patch('boto3.client')
    def test_process_s3_jsonl_batches_to_s3(self, mock_boto_client):
        # Prepare paths
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        sample_jsonl_path = os.path.join(data_dir, 'openfoodfacts-products-sample.jsonl')
        expected_json_path = os.path.join(data_dir, 'openfoodfacts-products-processed.json')

        # Read the sample .jsonl and gzip it in-memory
        with open(sample_jsonl_path, 'rb') as f:
            sample_jsonl_bytes = f.read()
        gzipped_bytes_io = io.BytesIO()
        with gzip.GzipFile(fileobj=gzipped_bytes_io, mode='wb') as gz:
            gz.write(sample_jsonl_bytes)
        gzipped_bytes_io.seek(0)

        # Mock S3 get_object to return our gzipped sample
        mock_s3 = MagicMock()
        mock_s3.get_object.return_value = {'Body': gzipped_bytes_io}
        mock_boto_client.return_value = mock_s3

        # Capture S3 put_object calls
        put_objects = []
        def put_object_side_effect(Bucket, Key, Body):
            put_objects.append((Key, Body))
        mock_s3.put_object.side_effect = put_object_side_effect

        # Run the batch processing (with small batch size for test)
        process_s3_jsonl_batches_to_s3(
            bucket='dummy-bucket',
            key='dummy-key',
            output_bucket='dummy-output-bucket',
            output_prefix='test-batch-',
            batch_size=1000
        )

        # Collect all processed objects from the batches
        processed = []
        for key, body in put_objects:
            batch = json.loads(body.decode('utf-8'))
            processed.extend(batch)

        # Load expected output
        with open(expected_json_path, 'r', encoding='utf-8') as f:
            expected = json.load(f)

        self.assertEqual(processed, expected)

if __name__ == "__main__":
    unittest.main() 