# Forkd

## Description
Forkd is a Chrome extension designed to make healthy grocery shopping easier. It helps users track their nutritional goals and make informed decisions while shopping online. 

## Development WIP
* Similar to how Yuka (phone application) displays nutrition information on products, metrics to be included in the browser alongside product information:
    * Environmental score 
    * Processed level
    * Nutrition score

* Possible implementation methods
    * Reads the DOM to get the UPC (unique product code) and then match the API lookup
    * Alternatively, scrapes the product description and matches similar products in our database


## Tasks

### Build Data Source in AWS 

* [x] Read documentation and request sample data from Open Food Facts APIs
    1. [OpenFoodFacts API Documentation](https://openfoodfacts.github.io/openfoodfacts-server/api/)

    2. [OpenFoodFacts Available Data](https://world.openfoodfacts.org/data)

    3. [Static OpenFoodFacts Field Descriptions from CSV](https://static.openfoodfacts.org/data/data-fields.txt)

    4. [OpenFoodFacts SDK for Node.js](https://github.com/openfoodfacts/openfoodfacts-nodejs/tree/develop/src/schemas)

* [x] Add Static JSON Unzipped File to S3 and Process with Glue in AWS

* [x] Query JSON data in Athena and explore dataset and columns of use in excel
    * Explore sample data in Excel sheet 

* [x] Document required columns in `architecture.drawio` for back-end data source

* [ ] Create lambda function to unzip and process data source
    * Export filtered data set of useful columns for US products and store in S3
    * Clean remaining dataset and remove AWS Glue table crawler



### Build logic to query similar products from data source

* [ ] Process and clean reduced data set for missing values or unnested rows

* [ ] Explore matching algorithms in Node.js

* [ ] Stem and tokenize product description text to utilize for the matching algorithm

* [ ] Build simple unit tests to check accuracy of matching algorithms against sample data



## Contact
- Project Link: [https://github.com/gordon-b-max/ThiccCheck](https://github.com/yourusername/ThiccCheck)
- Email: gordon.b.max@gmail.com
