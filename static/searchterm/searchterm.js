'use strict'

function handleResponse(data) {
    $('#tablecontainer').html(data);
}

function handleError(request) {
    if (typeof request === 'object' && request !== null) {
        alert('This website is using a security service to protect itself from online attacks. The action you just performed triggered the security solution. There are several actions that could trigger this block including submitting a certain word or phrase, a SQL command or malformed data.');
    } else {
        alert(request);
    }
}
let request = null
function getResults() {
    let query = $('#searchinput').val();
    let encodedquery = encodeURIComponent(query);
    let url = '/searchterm/results?query=' + encodedquery;
    if (request !== null)
        request.abort();
    let requestData = {
        type: 'GET',
        url: url, 
        success: handleResponse,
        error: handleError
    };
    request = $.ajax(requestData)
}

let timer = null;

function debouncedGetResults() {
    clearTimeout(timer);
    timer = setTimeout(getResults, 500);
}

function setup() {
    debouncedGetResults()
    $('#searchinput').on('input', debouncedGetResults);
}

$('document').ready(setup)