let currentCard = 1,
    totalCards = document.querySelectorAll('.card-container').length,
    infoback = document.querySelector(".info"),
    carousel = document.querySelector(".carousel"),
    next = document.querySelector(".next"),
    prev = document.querySelector(".prev"),
    flip = document.querySelector(".flip"),
    shuffleButton = document.querySelector(".shuffle"),
    opp = document.querySelector(".opp"),
    backButtons = document.querySelectorAll('.back-button');

let bool = false;

let allButtons = document.querySelectorAll('button');

updateCardCounter();

// Iterate over each button and set transition duration to 0
allButtons.forEach(button => {
    button.style.transitionDuration = '0s';
});

backButtons.forEach(button => {
    button.addEventListener('click', function() {
        resetCards();

        let car = document.querySelectorAll(".carousel");
        car.forEach(cardCar => {
            cardCar.style.transitionDuration='0s';
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

opp.addEventListener("click", function(e) {
    let currentCardElements = document.querySelectorAll(".card-container");
    currentCardElements.forEach(cardContainer => {
        cardContainer.querySelector(".card").style.transitionDuration='0s';
        cardContainer.querySelector(".card").classList.toggle("active");
    });

    // Check if the first card is active after toggling
    let firstCard = document.querySelector(".carousel .card-container:nth-child(" + currentCard + ") .card");
    bool = firstCard.classList.contains("active");
});


next.addEventListener("click", function(e) {
    resetSpeed();
    if (currentCard < document.querySelectorAll(".card-container").length) {
        resetCards();
        currentCard++;
        updateCardCounter();
        cardFly();
    }
});

prev.addEventListener("click", function(e) {
    resetSpeed();
    if (currentCard > 1) {
        resetCards();
        currentCard--;
        updateCardCounter();
        cardFly();
    }
});

flip.addEventListener("click", function (e) {
    resetSpeed();
    let currentCardElement = document.querySelector(".carousel .card-container:nth-child(" + currentCard + ") .card");
    if (currentCardElement) {
        currentCardElement.classList.toggle("active");
    }
});

document.querySelectorAll('.info').forEach(infoBackButton => {
    infoBackButton.addEventListener('click', function() {

        let currentCardElements = document.querySelectorAll(".card-container");
        currentCardElements.forEach((cardContainer, index) => {
            if (cardContainer.querySelector(".card").id == this.value) {
                createinfo(cardContainer.querySelector(".card"));
            }
        });
    });
});


shuffleButton.addEventListener("click", function(e) {
    resetCards();
    cardFly();
});

function createinfo(card){
    disableButtons();

    let extraInfo = "Term: " + card.querySelector('.back').textContent;; // Get the text content of the back of the card

    var modal = document.createElement("div");
    modal.classList.add("modal");

    var extraInfoContent = document.createElement("p");
    extraInfoContent.textContent = extraInfo;
    extraInfoContent.style.fontSize = "3vw";
    extraInfoContent.style.textAlign = "left";
    modal.appendChild(extraInfoContent);

    var extraInfoContent = document.createElement("p");
    extraInfo = "Memory aid: " + card.getAttribute('mem');
    extraInfoContent.textContent = extraInfo;
    extraInfoContent.style.fontSize = "1vw";
    extraInfoContent.style.textAlign = "left";
    modal.appendChild(extraInfoContent);

    var extraInfoContent = document.createElement("p");
    extraInfo = "Part of Speach: " + card.getAttribute('speach');
    extraInfoContent.textContent = extraInfo;
    extraInfoContent.style.fontSize = "1vw";
    extraInfoContent.style.textAlign = "left";
    modal.appendChild(extraInfoContent);

    var extraInfoContent = document.createElement("p");
    extraInfo = "Example Sentence: " + card.getAttribute('sentence');
    extraInfoContent.textContent = extraInfo;
    extraInfoContent.style.fontSize = "1vw";
    extraInfoContent.style.textAlign = "left";
    modal.appendChild(extraInfoContent);

    var closeButton = document.createElement("button");
    closeButton.textContent = "Close";
    closeButton.classList.add("close-button");
    closeButton.addEventListener("click", function() {
        enableButtons();
        modal.style.display = "none";
    });

    modal.appendChild(closeButton);

    document.body.appendChild(modal);
}


function disableButtons() {
    document.querySelectorAll('button').forEach(button => {
        button.disabled = true;
    });
}

function enableButtons() {
    document.querySelectorAll('button').forEach(button => {
        button.disabled = false;
    });
}

function resetSpeed() {
    let currentCardElements = document.querySelectorAll(".card-container");
    currentCardElements.forEach(cardContainer => {
        cardContainer.querySelector(".card").style.transitionDuration='.4s';
    });

    let car = document.querySelectorAll(".carousel");
        car.forEach(cardCar => {
            cardCar.style.transitionDuration='0.4s';
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
        }
        else card.classList.remove("active");
    });
}

function displayCard(cardnumber) {
    currentCard = cardnumber;
    updateCardCounter();
    cardFly();
}

function updateCardCounter() {
    document.getElementById('current-card').textContent = currentCard;
    document.getElementById('total-cards').textContent = totalCards;
}
