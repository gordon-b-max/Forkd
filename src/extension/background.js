// Background script for ThiccCheck extension
console.log('ThiccCheck background script loaded');

// Listen for tab updates
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    // Check if the URL is a supported grocery store
    // TODO: Implement URL checking logic
    console.log('Tab updated:', tab.url);
  }
});

// Handle messages from content script or popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'fetchNutritionalData') {
    // TODO: Implement API call to backend
    fetch('http://localhost:3000/api/nutrition', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(request.data)
    })
    .then(response => response.json())
    .then(data => sendResponse(data))
    .catch(error => sendResponse({ error: error.message }));
    return true; // Required for async response
  }
});
