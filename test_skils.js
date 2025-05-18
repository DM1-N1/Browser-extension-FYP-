let button = document.querySelector('#button1');
let url_text = document.querySelector('#url');
let prediction_text = document.querySelector('#prediction');
let confidence_text = document.querySelector('#confidence'); // Reference to the confidence section
let container = document.querySelector('.container'); // Reference to the container

function buttonpress() {
    console.log("Button Pressed");
    window.alert("You’re a smart person!");
}

function changePredictionText(prediction, confidence) {
    if (prediction === 1) {
        prediction_text.textContent = "The prediction is Phishing";
        confidence_text.textContent = `Confidence: ${(confidence * 100).toFixed(2)}%`; // Display confidence
        container.style.backgroundColor = "#ff4d4d"; // Red background for phishing
    } else if (prediction === 0) {
        prediction_text.textContent = "The prediction is Safe";
        confidence_text.textContent = `Confidence: ${(confidence * 100).toFixed(2)}%`; // Display confidence
        container.style.backgroundColor = "#4CAF50"; // Green background for safe
    } else {
        prediction_text.textContent = "Prediction result is unknown";
        confidence_text.textContent = "Confidence: Not available"; // Handle unknown confidence
        container.style.backgroundColor = "#dfe3e6"; // Neutral background for unknown
    }
}

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
getPrediction();