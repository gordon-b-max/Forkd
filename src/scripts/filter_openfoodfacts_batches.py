import json
import pandas as pd
import boto3
import io
from io import StringIO
from datetime import datetime


# AWS Configurations and Resources
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
s3_client = boto3.client('s3')
s3_bucket = 'thicc-check-processed-data'
s3_batches_directory = 'openfoodfacts-processed-output/processed-batches/'
s3_filtered_output = 'openfoodfacts-filtered-data/result.csv'


# Initiate fields to filter and save to S3
ids = []
product_names = []
nutriscore_grades = []
ecoscore_grades = []
nova_group_tags = []
countries = []
brands = []
categories = []


# Iterate through batches of JSON files to filter and reduce unused fields
response = s3_client.list_objects_v2(Bucket=s3_bucket, Prefix=s3_batches_directory)
batch_counter = 0

for obj in response['Contents']:

    batch_key = obj['Key']
    if batch_key.endswith('/'):
        print(f"Skipping directory object: {batch_key}")
        continue

    response_obj = s3_client.get_object(Bucket=s3_bucket, Key=batch_key)
    data = json.load(io.TextIOWrapper(response_obj['Body'], encoding='utf-8'))

    # Iterate through items in each batch to extract only desired fields
    for item in data:
        
        # Ignore items with missing id values
        if item.get('id') is None:
            continue

        # Ignore non-US foods
        if 'en:united-states' not in item.get('countries_hierarchy'):
            continue
            
        ids.append(item.get('id'))
        
        countries.append(item.get('countries_hierarchy'))
        
        nutriscore_grades.append(item.get('nutriscore_grade'))
        
        ecoscore_grades.append(item.get('ecoscore_grade'))
        
        product_names.append(item.get('product_name'))
        
        nova_group_tags.append(item.get('nova_groups_tags'))
        
        brands.append(item.get('brand_tags'))
        
        categories.append(item.get('categories_hierarchy'))

    # Print batch processed time
    print(f"Succesfully processed batch_{batch_counter}.json at time: {current_time} UTC")
    batch_counter += 1


# Create a DataFrame from desired fields and output as CSV
df = pd.DataFrame({
    "id": ids,
    "product_names": product_names,
    "nutriscore_grade": nutriscore_grades,
    "ecoscore_grade": ecoscore_grades,
    "nova_groups_tags": nova_group_tags,
    "countries_hierarchy": countries,
    "brand_tags": brands,
    "categories_hierarchy": categories
})
print("Sucessfully loaded filtered columns to dataframe")


# Save DataFrame to a CSV in memory
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)


# Upload the CSV to S3
s3_client.put_object(
    Bucket=s3_bucket,
    Key=s3_filtered_output,
    Body=csv_buffer.getvalue()
)
print(f"CSV uploaded to s3://{s3_bucket}/{s3_filtered_output}")



