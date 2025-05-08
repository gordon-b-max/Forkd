import json
import pandas as pd


# Initiate fields to filter and save to S3
ids = []
nutriscore_grades = []
ecoscore_grades = []
nova_group_tags = []
countries_hierarchies = []
brand_tags = []
categories_hierarchies = []
missing_value = "missing"



for i in range(2):

    with open(f'data/sample_batch_{i}.json', 'r') as f:
        data = json.load(f)

    # Iterate through items in each batch to extract only desired fields
    for item in data:

        # Ignore items with missing id values
        if item['id'] is None:
            continue

        # Ignore non-US foods
        if 'en:united-states' not in item.get('countries_hierarchy'):
            continue

        ids.append(item['id'])
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
    "nutriscore_grade": nutriscore_grades,
    "ecoscore_grade": ecoscore_grades,
    "nova_groups_tags": nova_group_tags,
    "countries_hierarchy": countries_hierarchies,
    "brand_tags": brand_tags,
    "categories_hierarchy": categories_hierarchies
})


# Save DataFrame to a CSV in memory
df.to_csv("test_result.csv", index=False)



