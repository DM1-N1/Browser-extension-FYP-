// References to DOM elements
let button = document.querySelector('#button1');
let url_text = document.querySelector('#url');
let prediction_text = document.querySelector('#prediction');
let confidence_text = document.querySelector('#confidence');
let container = document.querySelector('.container');
let reportButton = document.querySelector('#report-button');
let feedbackForm = document.querySelector('#feedback-form');
let mainInterface = document.querySelector('#main-interface');
let cancelFeedbackButton = document.querySelector('#cancel-feedback'); // Cancel button reference
let reportForm = document.querySelector('#report-form'); // Form reference

// Function to handle button press
function buttonpress() {
    console.log("Button Pressed");
    window.alert("You’re a smart person!");
}

// Function to update prediction and confidence text
function changePredictionText(prediction, confidence) {
    if (prediction === 1) {
        prediction_text.textContent = "The prediction is Phishing";
        confidence_text.textContent = `Confidence: ${(confidence * 100).toFixed(2)}%`;
        container.style.backgroundColor = "#ff4d4d"; // Red background for phishing
    } else if (prediction === 0) {
        prediction_text.textContent = "The prediction is Safe";
        confidence_text.textContent = `Confidence: ${(confidence * 100).toFixed(2)}%`;
        container.style.backgroundColor = "#4CAF50"; // Green background for safe
    } else {
        prediction_text.textContent = "Prediction result is unknown";
        confidence_text.textContent = "Confidence: Not available";
        container.style.backgroundColor = "#dfe3e6"; // Neutral background for unknown
    }
}

// Function to show the feedback form
function showFeedbackForm() {
    mainInterface.style.display = 'none';
    feedbackForm.style.display = 'block';
}

// Function to hide the feedback form
function hideFeedbackForm() {
    feedbackForm.style.display = 'none';
    mainInterface.style.display = 'block';
}

// Function to save the report data
function saveReport(reportData) {
    // Save the report to local storage
    let reports = JSON.parse(localStorage.getItem('reports')) || [];
    reports.push(reportData);
    localStorage.setItem('reports', JSON.stringify(reports));

    console.log("Report saved:", reportData);
}

// Function to handle form submission
function handleFormSubmission(event) {
    event.preventDefault(); // Prevent the form from refreshing the page

    // Get the form data
    let reportedUrl = document.querySelector('#reported-url').value;
    let correctClassification = document.querySelector('#correct-classification').value;

    // Save the report data
    let reportData = {
        url: reportedUrl,
        correct_classification: correctClassification,
        timestamp: new Date().toISOString()
    };

    saveReport(reportData);

    // Show a thank-you message
    alert("Thank you for your feedback!");

    // Reset the form and switch back to the main interface
    reportForm.reset();
    hideFeedbackForm();
}

function displaywarningpage(prediction) {
    if (prediction === 1) {
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            let currentTab = tabs[0]; // Get the current tab
            let currentUrl = currentTab.url; // Extract the URL of the current tab

            // Redirect to the warning page with the current URL as a parameter
            chrome.tabs.update({
                url: chrome.runtime.getURL(`warning_page.html?url=${encodeURIComponent(currentUrl)}`)
            });
        });
    }
}

// Function to fetch prediction and confidence
function getPrediction() {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        let currentTab = tabs[0]; // Get the current page/tab the user is viewing
        let currenturl = String(currentTab.url);
        url_text.textContent = `Current URL: ${currenturl}`;

        fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: currentTab.url })
        })
            .then(response => response.json())
            .then(data => {
                console.log("Prediction result:", data.prediction);
                console.log("Confidence level:", data.confidence);
                changePredictionText(data.prediction, data.confidence); // Pass confidence to the function
                displaywarningpage(data.prediction)
            })
            .catch(error => {
                console.error("Error fetching prediction:", error);
                prediction_text.textContent = "Error fetching prediction";
                confidence_text.textContent = "Confidence: Not available";
                container.style.backgroundColor = "#dfe3e6"; // Neutral background for errors
            });
    });
}

button.addEventListener('click', buttonpress);
reportButton.addEventListener('click', showFeedbackForm);
cancelFeedbackButton.addEventListener('click', hideFeedbackForm); 
reportForm.addEventListener('submit', handleFormSubmission); 

getPrediction();