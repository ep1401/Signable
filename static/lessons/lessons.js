const flashcard = document.getElementById('flashcard');
const nextBtn = document.getElementById('next');
const prevBtn = document.getElementById('prev');
const flipBtn = document.getElementById('flip');

let isFlipped = false;

nextBtn.addEventListener('click', () => {
  flashcard.style.transform = 'rotateY(180deg)';
  setTimeout(() => {
    flashcard.style.transform = 'rotateY(0deg)';
  }, 500); // Adjust timing as needed
});

prevBtn.addEventListener('click', () => {
  flashcard.style.transform = 'rotateY(-180deg)';
  setTimeout(() => {
    flashcard.style.transform = 'rotateY(0deg)';
  }, 500); // Adjust timing as needed
});

flipBtn.addEventListener('click', () => {
  if (!isFlipped) {
    flashcard.style.transform = 'rotateY(180deg)';
    isFlipped = true;
  } else {
    flashcard.style.transform = 'rotateY(0deg)';
    isFlipped = false;
  }
});
