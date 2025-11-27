/**
 * Content Script for Gmail Phishing Detector
 * 
 * This script runs in the context of the Gmail web page.
 * It monitors the DOM for email list items, extracts preview text,
 * sends it to the local backend API for analysis, and alerts the user
 * if a potential phishing attempt is detected.
 */

// Function to scan visible emails in the inbox.
function checkEmails() {
  // Select all email list items in the Gmail interface.
  // Gmail typically uses role="listitem" for email rows.
  const emails = document.querySelectorAll('div[role="listitem"]');

  // Iterate through each email element found.
  emails.forEach(email => {
    // Attempt to extract the email preview text.
    // The selector '.y6 span' is a common class for the subject/snippet in Gmail's DOM.
    // We use optional chaining (?.) to safely access innerText, defaulting to an empty string if not found.
    const preview = email.querySelector('.y6 span')?.innerText || "";

    // Check if we have preview text and if this email hasn't been checked yet.
    // We use a custom data attribute 'dataset.checked' to prevent re-scanning the same email.
    if (preview && !email.dataset.checked) {
      // Mark this email as processed.
      email.dataset.checked = "true";

      // Send the extracted text to the local Python backend for prediction.
      fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email_text: preview })
      })
        .then(response => response.json()) // Parse the JSON response from the server.
        .then(data => {
          // Check if either model flagged the email as "Phishing".
          if (data.RandomForest === "Phishing" || data.SGDClassifier === "Phishing") {
            // Create a visual warning indicator.
            const alertBox = document.createElement("div");
            alertBox.innerText = "⚠️ Warning: This email might be a phishing attempt!";

            // Style the alert box for high visibility.
            alertBox.style.color = "red";
            alertBox.style.fontWeight = "bold";
            alertBox.style.marginTop = "5px";
            alertBox.style.padding = "5px";
            alertBox.style.border = "1px solid red";
            alertBox.style.backgroundColor = "#ffe6e6";

            // Append the alert box to the email row in the DOM.
            email.appendChild(alertBox);
          }
        })
        .catch(error => {
          // Log any errors (e.g., backend not running) to the console for debugging.
          console.error("Error checking email:", error);
        });
    }
  });
}

// Set an interval to run the checkEmails function every 5 seconds.
// This is necessary because Gmail is a Single Page Application (SPA) that dynamically loads content
// without full page reloads, so we need to continuously scan for new emails.
setInterval(checkEmails, 5000);
