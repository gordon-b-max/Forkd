const ProductSearchService = require('../services/searchService');
const fs = require('fs').promises;
const path = require('path');

async function loadOpenFoodFactsData(filePath) {
    try {
        const data = await fs.readFile(filePath, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        console.error('Error loading OpenFoodFacts data:', error);
        throw error;
    }
}

async function main() {
    try {
        // Initialize the search service
        const searchService = new ProductSearchService();
        
        // Load your OpenFoodFacts data
        // Replace with your actual data file path
        const products = await loadOpenFoodFactsData('path_to_your_openfoodfacts_data.json');
        
        // Add products to the search index
        searchService.addProducts(products);
        
        // Example search
        const query = "Starbucks Iced Coffee, Medium Roast, Black, Unsweetened";
        const results = searchService.search(query);
        
        // Print results
        console.log(`Search results for: ${query}`);
        results.forEach((product, index) => {
            console.log(`${index + 1}. ${product.product_name} (Score: ${product.similarity_score.toFixed(2)})`);
        });
    } catch (error) {
        console.error('Error in main:', error);
    }
}

// Run the example
main(); 