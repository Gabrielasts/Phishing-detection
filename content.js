// Monitor Gmail inbox and detect phishing on email preview

function checkEmails() {
  // Gmail email list items usually inside divs with role="listitem"
  const emails = document.querySelectorAll('div[role="listitem"]');

  emails.forEach(email => {
    // Extract preview text (simplistic selector - may need adaptation)
    const preview = email.querySelector('.y6 span')?.innerText || "";

    if (preview && !email.dataset.checked) {
      email.dataset.checked = "true";  // Mark as checked to avoid duplicates
      
      // Send preview text to backend API for prediction
      fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email_text: preview })
      })
      .then(response => response.json())
      .then(data => {
        if (data.RandomForest === "Phishing" || data.SGDClassifier === "Phishing") {
          // Create alert box on the email item
          const alertBox = document.createElement("div");
          alertBox.innerText = "⚠️ Warning: This email might be a phishing attempt!";
          alertBox.style.color = "red";
          alertBox.style.fontWeight = "bold";
          alertBox.style.marginTop = "5px";
          email.appendChild(alertBox);
        }
      })
      .catch(console.error);
    }
  });
}

// Run check periodically as Gmail dynamically loads content
setInterval(checkEmails, 5000);
