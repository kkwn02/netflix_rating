
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url && tab.url.includes("netflix.com/browse")) {
    chrome.tabs.sendMessage(tabId, {}, (response) => {
      console.log(response["res"]);
    });
  }
});