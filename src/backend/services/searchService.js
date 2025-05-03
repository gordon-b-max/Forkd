const natural = require('natural');
const { TfIdf } = natural;
const stringSimilarity = require('string-similarity');

class ProductSearchService {
    constructor() {
        this.tfidf = new TfIdf();
        this.products = [];
        this.productTitles = [];
    }

    /**
     * Add products to the search index
     * @param {Array<Object>} products - Array of product objects
     */
    addProducts(products) {
        this.products = products;
        this.productTitles = products.map(product => product.product_name || '');
        
        // Add documents to TF-IDF
        this.productTitles.forEach(title => {
            this.tfidf.addDocument(title.toLowerCase());
        });
    }

    /**
     * Search for products using both TF-IDF and string similarity
     * @param {string} query - Search query
     * @param {number} topK - Number of results to return
     * @returns {Array<Object>} Array of products with similarity scores
     */
    search(query, topK = 10) {
        if (this.products.length === 0) {
            return [];
        }

        const processedQuery = this.preprocessQuery(query);
        
        // Calculate TF-IDF scores
        const tfidfScores = this.productTitles.map((title, index) => {
            let score = 0;
            this.tfidf.tfidfs(processedQuery, (i, measure) => {
                if (i === index) {
                    score = measure;
                }
            });
            return score;
        });

        // Calculate string similarity scores
        const similarityScores = this.productTitles.map(title => 
            stringSimilarity.compareTwoStrings(processedQuery, title.toLowerCase())
        );

        // Combine scores (adjust weights as needed)
        const combinedScores = tfidfScores.map((tfidfScore, i) => 
            0.7 * tfidfScore + 0.3 * similarityScores[i]
        );

        // Get top K results
        const results = combinedScores
            .map((score, index) => ({
                product: this.products[index],
                score
            }))
            .sort((a, b) => b.score - a.score)
            .slice(0, topK)
            .map(result => ({
                ...result.product,
                similarity_score: result.score
            }));

        return results;
    }

    /**
     * Preprocess the search query
     * @param {string} query - Original search query
     * @returns {string} Processed query
     */
    preprocessQuery(query) {
        // Remove special characters and extra spaces
        return query
            .toLowerCase()
            .replace(/[^\w\s]/g, ' ')
            .replace(/\s+/g, ' ')
            .trim();
    }
}

module.exports = ProductSearchService; 