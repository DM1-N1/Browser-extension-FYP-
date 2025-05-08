let button = document.querySelector('#button1')
let urlbutton = document.querySelector('#urlbutton')
let url_text = document.querySelector('#url')
let prediction_text = document.querySelector('#prediction')


function buttonpress() {
    console.log("YO")
    window.alert("Your a smart man")
}

function changePredictionText(prediction) {
    if (prediction === 1) {
        prediction_text.textContent = "The predicition is Phising";
    } else if (prediction === 0) {
        prediction_text.textContent = "The Prediciton is Safe";
    } else {
        prediction_text.textContent = "Prediction result is unkwown";
    }
}
function getPrediciton() {

    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        let currentTab = tabs[0]; // get the current page/tab the user is viewing
        let currenturl = String(currentTab.url);
        url_text.textContent = currenturl;


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
                changePredictionText(data.prediction)
            })
            .catch(error => {
                console.error("Error fetching prediction:", error);
            });
    }
    );


}

function addEventListener() {
    button.addEventListener('click', buttonpress);
    // urlbutton.addEventListener('click',geturl);
}

addEventListener()
getPrediciton()

// ignore this