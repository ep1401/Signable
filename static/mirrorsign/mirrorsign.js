'use strict';

            /* globals MediaRecorder */
            
            let mediaRecorder;
            let recordedBlobs;
            let isRecording = false;
            let countdownInterval;

            const errorMsgElement = document.querySelector('span#errorMsg');
            const videoElement = document.querySelector('video#recorded');
            const recordButton = document.querySelector('button#record2');

            recordButton.addEventListener('click', () => {
                recordButton.disabled = true;
                
                setTimeout(() => {
                    if (!isRecording) {
                        startRecording();
                    } else {
                        stopRecording();
                    }
                    
                    recordButton.disabled = false;
                }, 100); 
            });

            function playRecording() {
                const superBuffer = new Blob(recordedBlobs, { type: 'video/webm' });
                videoElement.src = null;
                videoElement.srcObject = null;
                videoElement.src = window.URL.createObjectURL(superBuffer);
                videoElement.controls = true;
                videoElement.loop = false;
                videoElement.play();
            }

            function handleDataAvailable(event) {
                console.log('handleDataAvailable', event);
                if (event.data && event.data.size > 0) {
                    recordedBlobs.push(event.data);
                    playRecording();
                }
            }

            async function startRecording() {
                recordedBlobs = [];
                let options = { mimeType: 'video/webm;codecs=vp9,opus' };
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                    mediaRecorder = new MediaRecorder(stream, options);
                    mediaRecorder.ondataavailable = handleDataAvailable;
                    mediaRecorder.start();
                    isRecording = true;
                    recordButton.textContent = 'Stop Recording';
                    videoElement.controls = false;
                    playStream(stream);
                    
                    
                    let duration = 20; 
                    countdownInterval = setInterval(() => {
                        if (duration <= 9)
                            document.getElementById('countdown').textContent = "0:0" + duration;
                        else
                        document.getElementById('countdown').textContent = "0:" + duration;
                        duration--;
                        if (duration < 0) {
                            stopRecording();
                        }
                    }, 1000); 
                } catch (e) {
                    console.error('Exception while creating MediaRecorder:', e);
                    alert('Recording is not supported on this browser. Please try on a different device.');
                    const stream = await navigator.mediaDevices.getUserMedia(constraints);
                    handleSuccess(stream);
                    return;
                }
            }
            
            function stopRecording() {
                mediaRecorder.stop();
                isRecording = false;
                recordButton.textContent = 'Record';
                clearInterval(countdownInterval); // Stop the countdown timer
                document.getElementById('countdown').textContent = ''; // Clear the countdown display
            }

            function handleSuccess(stream) {
                recordButton.disabled = false;
                console.log('getUserMedia() got stream:', stream);
                window.stream = stream;
                playStream(stream);
            }

            async function init(constraints) {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia(constraints);
                    handleSuccess(stream);
                } catch (e) {
                    console.error('navigator.getUserMedia error:', e);
                    alert("Webcam access denied")
                }
            }

            window.addEventListener("load", async () => {
                const constraints = {
                    video: {
                        width: 1280,
                        height: 1720
                    }
                };
                console.log('Using media constraints:', constraints);
                await init(constraints);
            });

function playStream(stream) {
    videoElement.srcObject = stream;
    videoElement.play();
}

    let currentCard = 1;
    let totalCards = document.querySelectorAll('.carousel-inner .carousel-item').length -1;
    let frontSideFirst = true; 

    
    function toggleSide() {
        frontSideFirst = !frontSideFirst; 
        $('.flashcard').each(function(index) {
            $(this).toggleClass('flipped', !frontSideFirst); 
        });
    }
    
    function resetCardSide() {
        if (frontSideFirst) {
            $('.carousel-item').eq(currentCard - 1).find('.flashcard').removeClass('flipped'); // Ensure front side is shown
        } else {
            $('.carousel-item').eq(currentCard - 1).find('.flashcard').addClass('flipped'); // Ensure back side is shown
        }
    }
    
    function updateCardCounter() {
        var counterContainer = document.getElementById('card-counter');
        counterContainer.textContent = currentCard + '/' + totalCards;
        counterContainer.style.fontSize = '25px';
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

    $('.info-button').on('click', function() {
        var flashcard = $(this).closest('.flashcard');

        var translation = flashcard.attr('mem');
        var memorytip = flashcard.attr('speech');
        var speech = flashcard.attr('sentence');

        var modalBody = $('#cardInfo');
        modalBody.html('');
        modalBody.append('<p><strong>Memory Tip:</strong> ' + translation + '</p>');
        modalBody.append('<p><strong>Part of Speech:</strong> ' + memorytip + '</p>');
        modalBody.append('<p><strong>Example Sentence:</strong> ' + speech + '</p>');
      });

      $(document).ready(function(){
        $('[data-bs-toggle="tooltip"]').tooltip();
    });

    
    $(document).ready(function(){
        updateCardCounter();
        $('.info-button').on('click', function(event){
            event.stopPropagation();
            $('#infoModal').modal('show');
        });
        $(document).on('click', '.flashcard', function(){
            if (!$(event.target).closest('.star-button').length) {
                $(this).toggleClass('flipped');
            }
        });
        
        $('.star-button').on('click', function(){
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
    });