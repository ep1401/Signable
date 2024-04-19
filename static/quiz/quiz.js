let cards = Array.from(document.querySelectorAll('.card-container'));
let score = 0;
let currentCardIndex = 0;
let totalCards = document.querySelectorAll('.card-container').length;

updateCardCounter();

// Randomize the order of the cards
cards.sort(() => Math.random() - 0.5);

// Hide all cards and show only the first one
cards.forEach((card, index) => {
  card.style.display = index === 0 ? 'block' : 'none';
});

// Add event listeners to the options
cards.forEach(card => {
  let options = card.querySelectorAll('.option');
  options.forEach(option => {
    option.addEventListener('click', function() {
      // Check if the selected option is correct
      if (option.dataset.correct) {
        score++;
      }
      // Disable all options after one is clicked
      options.forEach(option => {
        option.disabled = true;
      });
      // Show the next button
      document.getElementById('next-button').style.display = 'block';
    });
  });
});

// Add event listener to the next button
document.getElementById('next-button').addEventListener('click', function() {
  // Hide the current card
  cards[currentCardIndex].style.display = 'none';
  currentCardIndex++;
  updateCardCounter();
  if (currentCardIndex < cards.length) {
    // Show the next card
    cards[currentCardIndex].style.display = 'block';
    // Hide the next button until an option is clicked
    this.style.display = 'none';
  } else {
    // Quiz is over, show the score
    document.getElementById('score').textContent = `Quiz over! Your score is ${score}`;
    document.getElementById('score').style.display = 'block';
    this.style.display = 'none';
  }
});



function updateCardCounter() {
    document.getElementById('current-card').textContent = currentCardIndex + 1;
    document.getElementById('total-cards').textContent = totalCards;
}

