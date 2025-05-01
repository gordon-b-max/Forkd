// Content script for ThiccCheck extension
console.log('ThiccCheck content script loaded');

// Function to extract product information from the page
function extractProductInfo() {
  // TODO: Implement product information extraction
  // This will be specific to each grocery store website
  return {
    name: '',
    price: '',
    nutritionalInfo: {}
  };
}

// Listen for messages from the popup or background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getProductInfo') {
    const productInfo = extractProductInfo();
    sendResponse(productInfo);
  }
  return true; // Required for async response
});
