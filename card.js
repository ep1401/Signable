let cards = [
    {
        front: '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/NXRzRZFgSco" frameborder="0" allowfullscreen></iframe>',
        back: "HELLO"
    },
    {
        front: '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/NXRzRZFgSco" frameborder="0" allowfullscreen></iframe>',
        back: "HELLO"
    },
    {
        front: '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/NXRzRZFgSco" frameborder="0" allowfullscreen></iframe>',
        back: "HELLO"
    }
];

let currentCard = 1,
    carousel = document.querySelector(".carousel"),
    next = document.querySelector(".next"),
    prev = document.querySelector(".prev"),
    flip = document.querySelector(".flip");

renderCards();

function renderCards() {
    carousel.style.width = `${cards.length}00vw`;
    cards.map(el => {
        let div = document.createElement("div");
        div.classList.add("card");
        let front = document.createElement("div");
        front.classList.add("front");
        let back = document.createElement("div");
        back.classList.add("back");
        front.innerHTML = el.front;
        back.textContent = el.back;
        div.appendChild(front);
        div.appendChild(back);
        carousel.appendChild(div);
    });
}

next.addEventListener("click", function(e) {
    if (currentCard < cards.length) {
        currentCard++;
        cardFly();
    }
});

prev.addEventListener("click", function(e) {
    if (currentCard > 1) {
        currentCard--;
        cardFly();
    }
});

flip.addEventListener("click", function (e) {
    let currentCardElement = document.querySelector(".carousel .card:nth-child(" + currentCard + ")");
    if (currentCardElement) {
        currentCardElement.classList.toggle("active");
    }
});

function cardFly() {
    carousel.style.transform = `translateX(-${(currentCard - 1) * 100}vw)`;
}
