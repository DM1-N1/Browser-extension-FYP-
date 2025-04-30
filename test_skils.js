let button = document.querySelector('#button1')

button.addEventListener('click',geturl)

function geturl() {
    currenturl=window.location.href
    console.log(currenturl)
    return currenturl
}

// ignore this