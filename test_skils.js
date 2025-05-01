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

function addEventListener() {
    button.addEventListener('click', buttonpress);
    // urlbutton.addEventListener('click',geturl);
}

addEventListener()
geturl()

// ignore this