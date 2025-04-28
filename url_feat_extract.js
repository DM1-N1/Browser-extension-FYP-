// This will extract the url numertical features 



// Function to extract features from the URL
function extractUrlFeatures(url) {
    const a = document.createElement("a");
    a.href = url;
    const hostname = a.hostname || "";
    const path = a.pathname || "";

    // Extract the numerical domain (just the domain, without subdomains, etc.)
    const urlNumericDomain = a.hostname.split('.').slice(-2).join('.'); // Example: "example.com"

    // Only return numerical features
    return [
        urlNumericDomain,                                 // url_numeric_domain
        path.length,                                      // url_numeric_path_length
        hostname.split('.').length - 2,                   // url_numeric_num_subdomains
        /\d/.test(hostname) ? 1 : 0,                      // url_numeric_has_ip
        a.protocol === "https:" ? 1 : 0,                  // url_numeric_uses_https
        /[@\-=/]/.test(path) ? 1 : 0,                     // url_numeric_has_special_chars
    
    ];
}

// Function to handle prediction request
function getPrediction() {
    // Get the URL from the input field
    const urlInput = document.getElementById("url").value;
    
    // Validate URL
    if (!urlInput) {
        document.getElementById("prediction").innerHTML = "<span class='error'>Please enter a valid URL.</span>";
        return;
    }

    // Extract features from the URL
    const featuresArray = extractUrlFeatures(urlInput);
    
    // Create the data to send to the Flask API
    const data = { features: featuresArray };
    
    // Send the data to Flask API using AJAX (fetch)
    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        // Display the prediction result
        if (data.prediction !== undefined) {
            document.getElementById("prediction").innerHTML = "Prediction: " + data.prediction;
        } else {
            document.getElementById("prediction").innerHTML = "<span class='error'>Error: " + data.error + "</span>";
        }
    })
    .catch(error => {
        // Handle errors
        document.getElementById("prediction").innerHTML = "<span class='error'>Error occurred while fetching the prediction: " + error + "</span>";
    });
}
