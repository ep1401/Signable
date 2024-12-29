$(document).ready(function() {
  var maxFlashcards = $('.questionquiz').length;
  console.log(maxFlashcards)

  $('#questionCount').attr('max', maxFlashcards);
  $('#questionCount').on('input', function() {
      $('#questionCountOutput').text($(this).val());
  });



  function startNewQuiz() {
      $('.quiz-container').hide();
      $('#submitQuizBtn').hide();
      $('#startNewQuizBtn').hide();

     
  
      $('.slider-container').show();
      $('#startQuizBtn').show();
      $('label[for="questionCount"]').show();
      $('#questionCount').show();
      $('#questionCountOutput').show();
  }



  $('#startQuizBtn').click(function() {
      var sliderValue = parseInt($('#questionCount').val());
      $('.slider-container').hide();
      $('#startQuizBtn').hide();
      $('label[for="questionCount"]').hide();
      $('#questionCount').hide();
      $('#questionCountOutput').hide();
      $('.image-container').hide();
      $('#instructions').hide();

      $('.quiz-container').show();
      $('#submitQuizBtn').removeAttr('hidden');
      $('#submitQuizBtn').show();

      var flashcards = document.querySelectorAll('.questionquiz');

      flashcards =  Array.from(flashcards)
      var hideFlashcards = flashcards.slice(sliderValue, maxFlashcards)
      let selectFlashcards = flashcards.slice(0, sliderValue)
      

      hideFlashcards.forEach(function(flashcard, index) { 
      $(flashcard).hide()
  
      })

      selectFlashcards.forEach(function(flashcard, index) { 
      $(flashcard).addClass("activequestion")
  
      })


      $('.quiz-container').removeAttr('hidden');
      $('#submitContainer').removeAttr('hidden');
  });

  $('#submitQuizBtn').click(function() {
      var score = 0;
      var totalQuestions = parseInt($('#questionCount').val());
      var answeredQuestions = 0;
      var unansweredQuestionNumbers = []; 
  
      $('.activequestion').each(function(index) {
          var selectedOption = $(this).find('input[type="radio"]:checked');
  
          if (selectedOption.length > 0) {
              answeredQuestions++;
          } else {
              unansweredQuestionNumbers.push(index + 1);
          }
      });
  
      if (answeredQuestions < totalQuestions) {
          var message = 'Please answer the following question(s) before submitting:\n';
          unansweredQuestionNumbers.forEach(function(number) {
              message += 'Question ' + number + '\n';
          });
          alert(message);
          return; 
      }
  
      answeredQuestions = 0;
  
      $('.activequestion').each(function() {
          var selectedOption = $(this).find('input[type="radio"]:checked');
      
          $(this).find('input[type="radio"]').prop('disabled', true);
      
          if (selectedOption.length > 0) {
              if (selectedOption.val() === 'correct') {
                  selectedOption.next('span').addClass('correct-answer');
                  selectedOption.next('span').prepend('<i class="fas fa-check"></i> ');
                  score++;
              } else {
                  selectedOption.next('span').addClass('incorrect-answer').prepend('<i class="fas fa-times"></i> ');
                  $(this).find('input[value="correct"]').next('span').addClass('correct-answer');
                  $(this).find('input[value="correct"]').next('span').prepend('<i class="fas fa-check"></i> ');
              }
          }
      });
  
      var scoreMessage = 'Your score: ' + score + ' out of ' + totalQuestions;
      $('#scoreMessage').text(scoreMessage);
      $('#submitQuizBtn').hide();
      $('#startNewQuizBtn').removeAttr('hidden');
      $('#startNewQuizBtn').show();
      $('#scoreModal').modal('show'); 

  });


});