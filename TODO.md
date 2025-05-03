# MVP Sequential Task List with Subtasks

## Backend Logic

### Tasks
1.  Build Data Source in AWS 

    * [Done] Read documentation and request sample data from Open Food Facts APIs
        1. [OpenFoodFacts API Documentation](https://openfoodfacts.github.io/openfoodfacts-server/api/)

        2. [OpenFoodFacts Available Data](https://world.openfoodfacts.org/data)

        1. [Static OpenFoodFacts Field Descriptions from CSV](https://static.openfoodfacts.org/data/data-fields.txt)

        4. [OpenFoodFacts SDK for Node.js](https://github.com/openfoodfacts/openfoodfacts-nodejs/tree/develop/src/schemas)

    * [Done] Add Static JSON Unzipped File to S3 and Process with Glue in AWS

    * [*In-progress*] Query JSON data in Athena and explore dataset and columns of use in excel
    
    * [ ] Document required columns in `architecture.drawio` for back-end data source

    * [ ] Create filtered data set of useful columns for US products and store in S3


2.  Build logic to query similar products from data source

    * [ ] Process and clean reduced data set for missing values or unnested rows
    
    * [ ] Explore matching algorithms in Node.js

    * [ ] Stem and tokenize product description text to utilize for the matching algorithm

    * [ ] Build simple unit tests to check accuracy of matching algorithms against sample data















