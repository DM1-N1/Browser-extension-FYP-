let button = document.querySelector('#button1')
let urlbutton = document.querySelector('#urlbutton')
let url_text = document.querySelector('#url')


function buttonpress() {
    console.log("YO")
    window.alert("Your a smart man")
}



// function geturl() {
//     chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
//         let currentTab = tabs[0]; // get the current page/tab the user is viewing
//         let currenturl = String(currentTab.url);
//         url_text.textContent = currenturl; 
//         console.log("Current URL:", currentTab.url);
//     });

// }

// function writeUrlToTextFile(url) {
//     debugger;
//     let passedUrl = String(url);
//     let blob = new Blob([passedUrl], { type: 'text/plain' });
//     let urlObject = URL.createObjectURL(blob);

//     chrome.downloads.download({
//         url: urlObject,
//         filename: 'url.txt',
//         conflictAction: 'overwrite' // Ensures the file is overwritten
//     }, function() {
//         console.log('URL written to url.txt:', passedUrl);
//     });
// }

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