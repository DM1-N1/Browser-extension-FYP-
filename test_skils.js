let button = document.querySelector('#button1')
let urlbutton = document.querySelector('#urlbutton')


function buttonpress() {
    console.log("YO")
    window.alert("Your a smart man")
}



function geturl() {
    currenturl=window.location.href
    console.log("This is the ", currenturl)
    return currenturl
}

function addEventListener() {
    button.addEventListener('click',buttonpress);
    urlbutton.addEventListener('click',geturl);
}

addEventListener()

// ignore this