'use strict'

function handleResponse(data) {
    $('#tablecontainer').html(data);
}

function handleError(request) {
    console.log(request)
    
    if (request.statusText !== 'abort') {
        alert('Error: Failed to fetch data from server')
    }
    else if (request.status === 403) {
        alert("A 403 Forbidden Resource Error Occured Invalid Input");;
    }
    else {
        alert(request)
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