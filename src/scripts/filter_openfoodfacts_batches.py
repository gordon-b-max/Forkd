import json
import pandas as pd
import boto3
import io
from io import StringIO


def lambda_handler(event, context):

    # AWS Configurations and Resource locations
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
    countries_hierarchies = []
    brand_tags = []
    categories_hierarchies = []


    # Iterate through batches of JSON files to filter and reduce unused fields
    response = s3_client.list_objects_v2(Bucket=s3_bucket, Prefix=s3_batches_directory)

    for obj in response['Contents']:

        batch_key = obj['Key']

        response_obj = s3_client.get_object(Bucket=s3_bucket, Key=batch_key)
        data = json.load(io.TextIOWrapper(response_obj['Body'], encoding='utf-8'))

        # Iterate through items in each batch to extract only desired fields
        for item in data:

            # Ignore items with missing id values
            if item['id'] is None:
                continue

            # Ignore non-US foods
            if 'en:united-states' not in item.get('countries_hierarchy'):
                continue

            ids.append(item['id'])
            product_names.append(item.get('product_name'))
            nutriscore_grades.append(item.get('nutriscore_grade'))
            ecoscore_grades.append(item.get('ecoscore_grade'))

            # Remove double quotes for arrays with multiple values
            nova_group = [item.get('nova_groups_tags')] if isinstance(item.get('nova_groups_tags'), str) else item.get('nova_groups_tags')
            nova_group_tags.append(nova_group)

            countries_hierarchy = [item.get('countries_hierarchy')] if isinstance(item.get('countries_hierarchy'), str) else item.get('countries_hierarchy')
            countries_hierarchies.append(countries_hierarchy)

            brand_tag = [item.get('brand_tags')] if isinstance(item.get('brand_tags'), str) else item.get('brand_tags')
            brand_tags.append(brand_tag)

            category_hierarchy = [item.get('categories_hierarchy')] if isinstance(item.get('categories_hierarchy'), str) else item.get('categories_hierarchy')
            categories_hierarchies.append(category_hierarchy)


    # Create a DataFrame from desired fields and output as CSV
    df = pd.DataFrame({
        "id": ids,
        "product_names": product_names,
        "nutriscore_grade": nutriscore_grades,
        "ecoscore_grade": ecoscore_grades,
        "nova_groups_tags": nova_group_tags,
        "countries_hierarchy": countries_hierarchies,
        "brand_tags": brand_tags,
        "categories_hierarchy": categories_hierarchies
    })


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



