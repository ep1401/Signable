document.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>');

// Include AWS SDK
document.write('<script src="https://sdk.amazonaws.com/js/aws-sdk-2.1078.0.min.js"></script>');


let s3;
let theStream;
let theRecorder;
let recordedChunks = [];
let blob = null;
let url = null;
let camera = 'front'; // front, back
let allElements = '.video-record .video-playback .record-btn .go-back-btn .toggle-cam-btn .progress-btn .download-btn .upload-btn .stop-btn';
let config = {
    bucket: 'video-upload-6052019',
    region: 'us-east-1',
    identityPoolId: 'us-east-1:0dce9491-45ec-4e98-9f36-cfc7cf7bc70e'
};
let currentCard = 1,
    infofront = document.querySelector(".info-front"),
    infoback = document.querySelector(".info-back"),
    carousel = document.querySelector(".carousel"),
    next = document.querySelector(".next"),
    prev = document.querySelector(".prev"),
    flip = document.querySelector(".flip"),
    btn_stop_record = document.querySelectorAll(".stop-btn"),
    btn_record_btn = document.querySelectorAll(".record-btn"),
    go_back_btn = document.querySelectorAll(".go-back-btn"),
    backButtons = document.querySelectorAll('.back-button');

let bool = false;
let stopped = false;
let recording = false;
let id = 0;

btn_stop_record.forEach(button => {
    button.addEventListener('click', function() {
        onStreamStop(currentCard);
    });
});

btn_record_btn.forEach(button => {
    button.addEventListener('click', function() {
        onStreamRecord(currentCard);
    });
});

go_back_btn.forEach(button => {
    button.addEventListener('click', function() {
        onBackClick(currentCard);
    });
});

backButtons.forEach(button => {
    button.addEventListener('click', function() {
        resetCards();

        let car = document.querySelectorAll(".carousel");
        car.forEach(cardCar => {
            cardCar.style.transitionDuration = '0s';
        });

        let currentCardElements = document.querySelectorAll(".card-container");
        currentCardElements.forEach((cardContainer, index) => {
            if (cardContainer.querySelector(".card").id == this.value) {
                currentCard = index + 1;
            }
        });

        cardFly();
    });
});

next.addEventListener("click", function(e) {
    if (stopped) {
        stopped = false;
        showElements('.video-record .record-btn');
        getStream();
    }

    if (recording) {
        onStreamStop(id);
        return;
    }

    resetSpeed();
    if (currentCard < document.querySelectorAll(".card-container").length) {
        resetCards();
        currentCard++;
        cardFly();
    }
});

prev.addEventListener("click", function(e) {
    if (stopped) {
        stopped = false;
        showElements('.video-record .record-btn');
        getStream();
    }

    if (recording) {
        onStreamStop(id);
        return;
    }

    resetSpeed();
    if (currentCard > 1) {
        resetCards();
        currentCard--;
        cardFly();
    }
});

flip.addEventListener("click", function(e) {
    resetSpeed();
    let currentCardElement = document.querySelector(".carousel .card-container:nth-child(" + currentCard + ") .card");
    if (currentCardElement) {
        currentCardElement.classList.toggle("active");
    }
});

document.querySelectorAll('.info-back').forEach(infoBackButton => {
    infoBackButton.addEventListener('click', function() {
        // Extract the ID of the current card
        let currentCardId = infoBackButton.closest('.card-container').querySelector('.card').back;

        // Retrieve extra information for the current card (assuming you have a way to obtain it)
        let extraInfo = "heeeee\n\nasdf\n\n"; // Replace this with the method to retrieve extra information based on the currentCardId

        // Create a modal to display the extra information
        var modal = document.createElement("div");
        modal.classList.add("modal");

        // Display the extra information in the modal
        var extraInfoContent = document.createElement("p");
        extraInfoContent.textContent = extraInfo;
        modal.appendChild(extraInfoContent);

        // Create a close button for the modal
        var closeButton = document.createElement("button");
        closeButton.textContent = "Close";
        closeButton.classList.add("close-button");
        closeButton.addEventListener("click", function() {
            modal.style.display = "none";
        });

        // Append the close button to the modal
        modal.appendChild(closeButton);

        // Append the modal to the body
        document.body.appendChild(modal);
    });
});

function resetSpeed() {
    let currentCardElements = document.querySelectorAll(".card-container");
    currentCardElements.forEach(cardContainer => {
        cardContainer.querySelector(".card").style.transitionDuration = '.4s';
    });

    let car = document.querySelectorAll(".carousel");
    car.forEach(cardCar => {
        cardCar.style.transitionDuration = '0.4s';
    });
}

function cardFly() {
    carousel.style.transform = `translateX(-${(currentCard - 1) * 100}vw)`;
}

function resetCards() {
    let cards = document.querySelectorAll(".card-container .card");
    cards.forEach(card => {
        if (bool) {
            card.classList.add("active");
        } else card.classList.remove("active");
    });
}

function displayCard(cardnumber) {
    currentCard = cardnumber;
    cardFly();
}

$(function() {
    // Initialise Bucket
    setupBucket();

    // Get stream
    getStream();
});



function onBackClick() {
    stopped = false;
    recording = false;
    showElements('.video-record .record-btn');
    getStream();
}

function onStreamRecord(cardId) {
    recording = true;
    id = cardId;
    showElements(`#video-record-${cardId} .stop-btn`);
    recordedChunks = [];

    try {
        theRecorder = new MediaRecorder(theStream, { mimeType: "video/webm" });
    } catch (e) {
        console.error('Exception while creating MediaRecorder: ' + e);
        return;
    }

    console.log('MediaRecorder created');
    theRecorder.ondataavailable = function(event) {
        recorderOnDataAvailable(event, cardId);
    };
    theRecorder.start(100);
}

function onStreamStop(cardId) {
    stopped = true;
    recording = false;
    showElements(`#video-playback-${cardId} .go-back-btn`);

    console.log('Saving data');
    theRecorder.stop();
    stopAllMediaTracks();

    blob = new Blob(recordedChunks, { type: "video/webm" });
    url = (window.URL || window.webkitURL).createObjectURL(blob);

    var mediaControl = document.getElementById(`video-playback-${cardId}`);
    mediaControl.src = url;
}



/**
 * Helpers
 */
function setupBucket() {
    var albumBucketName = config.bucket;
    var bucketRegion = config.region;
    var IdentityPoolId = config.identityPoolId;

    AWS.config.update({
        region: bucketRegion,
        credentials: new AWS.CognitoIdentityCredentials({
            IdentityPoolId: IdentityPoolId
        })
    });

    s3 = new AWS.S3({
        apiVersion: '2006-03-01',
        params: { Bucket: albumBucketName }
    });
}

function recorderOnDataAvailable(event) {
    if (event.data.size == 0) return;
    console.log('ondataavailable, type: ' + event.data.type);
    recordedChunks.push(event.data);
}

function getUserMedia(options, successCallback, failureCallback) {
    navigator.mediaDevices.getUserMedia(options).then(successCallback, failureCallback);
}

function getStream() {
    var facingMode = camera === 'front' ? { facingMode: "user" } : { facingMode: "environment" };
    var constraints = { video: facingMode, audio: true };

    // Loop through each card to get the corresponding video-record element
    document.querySelectorAll('.video-record').forEach(videoRecord => {
        getUserMedia(constraints, function(stream) {
            var mediaControl = videoRecord;
            if (navigator.mozGetUserMedia) {
                mediaControl.mozSrcObject = stream;
            } else {
                mediaControl.srcObject = stream;
            }

            theStream = stream;
        }, function(err) {
            alert('Error: ' + err);
        });
    });
}

function showElements(elements) {
    hideElements(allElements);

    elements.split(" ").forEach(e => {
        $(e).css({
            'display': 'flex'
        });
    });
}

function hideElements(elements) {
    elements.split(" ").forEach(e => {
        $(e).css({
            'display': 'none'
        });
    });
}

function stopAllMediaTracks() {
    theStream.getTracks().forEach(track => track.stop());
}
