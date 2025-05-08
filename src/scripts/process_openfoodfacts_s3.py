import boto3
import gzip
import json

# AWS Resources Configured
bucket = 'thicc-check-open-food--data'
key = 'zipped-openfoodfacts-data/openfoodfacts-products.jsonl.gz'
output_bucket = 'thicc-check-processed-data'
output_prefix = 'openfoodfacts-processed-output/processed-batches/batch_'
batch_size = 10000

def extractFields(product):
    id_value = product.get("_id") or product.get("id") or product.get("code") or "unknown"
    return {
        "id": id_value,
        "product_name": product.get("product_name", "unknown"),
        "nutriments": product.get("nutriments", "unknown"),
        "nutriscore": product.get("nutriscore", "unknown"),
        "nutriscore_data": product.get("nutriscore_data", "unknown"),
        "nutriscore_grade": product.get("nutriscore_grade", "unknown"),
        "ecoscore_grade": product.get("ecoscore_grade", "unknown"),
        "ecoscore_data": product.get("ecoscore_data", "unknown"),
        "nova_groups_tags": product.get("nova_groups_tags", "unknown"),
        "brand_tags": product.get("brands_tags", "unknown"),
        "categories_hierarchy": product.get("categories_hierarchy", "unknown"),
        "countries_hierarchy": product.get("countries_hierarchy", "unknown"),
        "image_url": product.get("image_url", "unknown")
    }

def process_s3_jsonl_batches_to_s3(bucket, key, output_bucket, output_prefix, batch_size):
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=key)
    body = response['Body']

    batch = []
    batch_num = 0
    with gzip.GzipFile(fileobj=body) as gz:
        for i, line in enumerate(gz, 1):
            try:
                product = json.loads(line)
                fields = extractFields(product)
                batch.append(fields)
            except json.JSONDecodeError:
                continue
            if i % batch_size == 0:
                # Write batch to S3
                s3.put_object(
                    Bucket=output_bucket,
                    Key=f"{output_prefix}{batch_num}.json",
                    Body=json.dumps(batch, ensure_ascii=False).encode('utf-8')
                )
                print(f"Wrote batch {batch_num} to S3")
                batch = []
                batch_num += 1
        # Write any remaining
        if batch:
            s3.put_object(
                Bucket=output_bucket,
                Key=f"{output_prefix}{batch_num}.json",
                Body=json.dumps(batch, ensure_ascii=False).encode('utf-8')
            )
            print(f"Wrote final batch {batch_num} to S3")

    print("Done! All batches written to S3.")

if __name__ == "__main__":
    process_s3_jsonl_batches_to_s3(bucket, key, output_bucket, output_prefix, batch_size) 








    