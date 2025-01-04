'use strict'

function handleResponse(data) {
    $('#tablecontainer').html(data);
}

function handleError(xhr, textStatus, errorThrown) {
    if (xhr.responseText && xhr.responseText.startsWith("<")) {
        alert('This website is using a security service to protect itself from online attacks. The action you just performed triggered the security solution. There are several actions that could trigger this block including submitting a certain word or phrase, a SQL command or malformed data.');
    }
    else {
        alert("Error while fetching data from the server. Please contact a system adminstrator");
    }
}

let request = null;
let lessonid = $("#lesson-info").data("lesson");  // Fetching from the data-attribute
let courseid = $("#lesson-info").data("course");      // Convert to a proper JSON format

function getResults() {
    let query = $('#searchinput').val();
    let encodedquery = encodeURIComponent(query);
    let url = '/lessons/results?query=' + encodedquery + '&lessonid=' + lessonid + '&courseid=' + courseid;
    if (request !== null)
        request.abort();
    let requestData = {
        type: 'GET',
        url: url,
        success: handleResponse,
        error: handleError
    };
    request = $.ajax(requestData);
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

            let currentCard = 1;
let totalCards = document.querySelectorAll('.carousel-inner .carousel-item').length;
let frontSideFirst = true; 

let shuffleButton = document.querySelector(".shuffle");
shuffleButton.addEventListener("click", shuffleCards);

let oppButton = document.querySelector(".opp");
oppButton.addEventListener("click", toggleSide);

function shuffleCards() {
    let cardContainers = Array.from(document.querySelectorAll(".carousel-item"));
    let shuffledCards = shuffleArray(cardContainers);
    $('.carousel-inner').empty();
    shuffledCards.forEach(card => {
        $('.carousel-inner').append(card);
    });
    $('.carousel-item').removeClass('active'); 
    $('.carousel-item').first().addClass('active'); 
    totalCards = document.querySelectorAll('.carousel-inner .carousel-item').length; 
    currentCard = 1; 
    updateCardCounter();
    resetCardSide();
}

function toggleSide() {
    frontSideFirst = !frontSideFirst; 
    $('.flashcard').each(function(index) {
        $(this).toggleClass('flipped', !frontSideFirst); 
    });
}

function resetCardSide() {
    if (frontSideFirst) {
        $('.carousel-item').eq(currentCard - 1).find('.flashcard').removeClass('flipped'); 
    } else {
        $('.carousel-item').eq(currentCard - 1).find('.flashcard').addClass('flipped'); 
    }
}

$('.carousel-control-prev').on('click', function() {
    if (currentCard > 1) {
        currentCard--;
    }
    else {
        currentCard = totalCards;
    }
    resetCardSide();
    updateCardCounter();
});

$('.carousel-control-next').on('click', function() {
    if (currentCard < totalCards) {
        currentCard++;
    }
    else {
        currentCard = 1;
    }
    resetCardSide(); 
    updateCardCounter();
});


function shuffleArray(array) {
    let currentIndex = array.length, temporaryValue, randomIndex;
  
    while (0 !== currentIndex) {
  
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex -= 1;
  
      temporaryValue = array[currentIndex];
      array[currentIndex] = array[randomIndex];
      array[randomIndex] = temporaryValue;
    }
  
    return array;
}

function updateCardCounter() {
    var counterContainer = document.getElementById('card-counter');
    counterContainer.textContent = currentCard + '/' + totalCards;
    counterContainer.style.fontSize = '25px';
}

$(document).ready(function(){
    $('[data-bs-toggle="tooltip"]').tooltip();
});

$(document).ready(function(){
    updateCardCounter();
});

$(document).on('click', '.info-button', function(event){
    event.stopPropagation();
    var flashcard = $(this).closest('.flashcard');

    var translation = flashcard.attr('mem');
    var memorytip = flashcard.attr('speech');
    var speech = flashcard.attr('sentence');

    var modalBody = $('#cardInfo');
    modalBody.html('');
    modalBody.append('<p><strong>Memory Tip:</strong> ' + translation + '</p>');
    modalBody.append('<p><strong>Part of Speech:</strong> ' + memorytip + '</p>');
    modalBody.append('<p><strong>Example Sentence:</strong> ' + speech + '</p>');
    $('#infoModal').modal('show'); 
});

$(document).on('click', '.flashcard', function(event){
    if (!$(event.target).closest('.star-button').length) {
        $(this).toggleClass('flipped');
    }
});

$(document).on('click', '.star-button', function(event){
    event.stopPropagation();
    var card = $(this).closest('.flashcard');
    let cardid = card.attr("id")
    let lessonid = "{{ lesson_num }}";
    let courseid = "{{ course }}";
    var frontStar = card.find('.front .star-button');
    var backStar = card.find('.back .star-button');
    frontStar.attr("disabled", "disabled");
    backStar.attr("disabled", "disabled");

    // Toggle active class for star button
    $(this).toggleClass('active');

    // Toggle active class for front and back stars
    if ($(this).hasClass('active')) {


        var csrf_token = "{{ csrf_token() }}";

            $.ajaxSetup({
             beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
                        }
             }})




        $.ajax({
            url: "/addstarredflashcard",
            type: 'PUT',    
            data: JSON.stringify({"cardid": cardid, "courseid": courseid, "lessonid": lessonid}),
            contentType: "application/JSON",
            success: function(data) {
                frontStar.removeAttr("disabled");
                backStar.removeAttr("disabled");
                frontStar.addClass('active');
                backStar.addClass('active');
            }, 
            error: function(data) {
                frontStar.removeAttr("disabled");
                backStar.removeAttr("disabled");
                frontStar.removeClass('active');
                backStar.removeClass('active');
                alert("An error occurred and the review stack was not updated. Please try again or refresh the page");
            }
        });
          
    } else {



        var csrf_token = "{{ csrf_token() }}";

            $.ajaxSetup({
             beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
                        }
             }})


        $.ajax({
            url: "/deletestarredflashcard",
            type: 'PUT',    
            data: JSON.stringify({"cardid": cardid}),
            contentType: "application/JSON",
            success: function(data) {
                frontStar.removeAttr("disabled");
                backStar.removeAttr("disabled");
                frontStar.removeClass('active');
                backStar.removeClass('active');
            },
            error: function(data) {
                frontStar.removeAttr("disabled");
                backStar.removeAttr("disabled");
                frontStar.addClass('active');
                backStar.addClass('active');
                alert("An error occurred and the review stack was not updated. Please try again or refresh the page");
            }
        });
       
    }
});
