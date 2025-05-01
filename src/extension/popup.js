document.addEventListener('DOMContentLoaded', function() {
  const analyzeBtn = document.getElementById('analyzeBtn');
  const productInfo = document.getElementById('productInfo');

  analyzeBtn.addEventListener('click', async () => {
    // Get the active tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    // Send message to content script to get product info
    chrome.tabs.sendMessage(tab.id, { action: 'getProductInfo' }, async (response) => {
      if (response) {
        // Send product info to background script for processing
        chrome.runtime.sendMessage(
          { action: 'fetchNutritionalData', data: response },
          (nutritionalData) => {
            if (nutritionalData.error) {
              productInfo.innerHTML = `<p>Error: ${nutritionalData.error}</p>`;
            } else {
              // TODO: Format and display nutritional data
              productInfo.innerHTML = `
                <h3>${response.name}</h3>
                <p>Price: ${response.price}</p>
                <p>Nutritional Information:</p>
                <pre>${JSON.stringify(nutritionalData, null, 2)}</pre>
              `;
            }
          }
        );
      } else {
        productInfo.innerHTML = '<p>No product information found on this page</p>';
      }
    });
  });
});
