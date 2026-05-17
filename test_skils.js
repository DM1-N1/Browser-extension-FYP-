let button = document.querySelector('#button1')
let urlbutton = document.querySelector('#urlbutton')
let url_text = document.querySelector('#url')
let prediction_text = document.querySelector('#prediction')

const DEFAULT_SERVER_URLS = ['http://127.0.0.1:5000', 'http://localhost:5000']
const PREDICT_ENDPOINT = '/predict'

function buttonpress() {
    console.log('YO')
    window.alert('Your a smart man')
}

function changePredictionText(prediction) {
    if (prediction === 1) {
        prediction_text.textContent = 'The predicition is Phising'
    } else if (prediction === 0) {
        prediction_text.textContent = 'The Prediciton is Safe'
    } else {
        prediction_text.textContent = 'Prediction result is unkwown'
    }
}

function buildPredictUrl(baseUrl) {
    return baseUrl.replace(/\/$/, '') + PREDICT_ENDPOINT
}

function getConfiguredServerUrls() {
    if (typeof getServerUrls === 'function') {
        return getServerUrls().filter(Boolean)
    }
    return []
}

async function fetchPrediction(urls, payload) {
    for (const baseUrl of urls) {
        try {
            const response = await fetch(buildPredictUrl(baseUrl), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            })

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`)
            }

            return await response.json()
        } catch (error) {
            console.warn(`Server request failed for ${baseUrl}:`, error)
        }
    }

    throw new Error(`Could not reach prediction server. Tried: ${urls.join(', ')}`)
}

function getPrediciton() {
    chrome.tabs.query({ active: true, currentWindow: true }, async function (tabs) {
        let currentTab = tabs[0]
        let currenturl = String(currentTab.url)
        url_text.textContent = currenturl

        const configuredUrls = getConfiguredServerUrls()
        const serverUrls = [...new Set([...DEFAULT_SERVER_URLS, ...configuredUrls])]

        try {
            const data = await fetchPrediction(serverUrls, { url: currentTab.url })
            console.log('Prediction result:', data.prediction)
            changePredictionText(data.prediction)
        } catch (error) {
            console.error('Error fetching prediction:', error)
            prediction_text.textContent = 'Error connecting to backend server'
        }
    })
}

function addEventListener() {
    button.addEventListener('click', buttonpress)
    // urlbutton.addEventListener('click',geturl);
}

addEventListener()
getPrediciton()

// ignore this