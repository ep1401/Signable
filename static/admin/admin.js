function checkInput() {
    document.getElementById("submitButton").disabled = true;
    let translation_input = $("#translationinput").val();
    let isvalid = true;

    if ($("#courseinput").val() === null) {
        $("#courseinput").addClass("is-invalid");
        isvalid = false;
    } else {
        $("#courseinput").removeClass("is-invalid");
    }

    if (translation_input.length > 300 || translation_input.length === 0) {
        if (translation_input.length === 0) {
            $("#translationfeedback").empty();
            $("#translationfeedback").html("Please enter an ASL translation");
        } else {
            $("#translationfeedback").empty();
            $("#translationfeedback").html("Please limit the translation to less than 50 words");
        }
        $("#translationinput").addClass("is-invalid");
        isvalid = false;
    } else {
        $("#translationinput").removeClass("is-invalid");
    }

    let link_input = $("#videolinkinput").val();

    if (link_input.length === 0) {
        $("#videolinkinput").addClass("is-invalid");
        isvalid = false;
    } else {
        $("#videolinkinput").removeClass("is-invalid");
    }

    let lesson_input = $("#lessonnumberinput").val();

    if (lesson_input.length === 0) {
        $("#lessonnumberinput").addClass("is-invalid");
        isvalid = false;
    } else {
        $("#lessonnumberinput").removeClass("is-invalid");
    }

    let mem_tip = $("#memoryinput").val();
    if (mem_tip.length > 300) {
        $("#memoryinput").addClass("is-invalid");
        isvalid = false;
    } else {
        $("#memoryinput").removeClass("is-invalid");
    }

    let sentence_input = $("#sentenceinput").val();
    if (sentence_input.length > 300) {
        $("#sentenceinput").addClass("is-invalid");
        isvalid = false;
    } else {
        $("#sentenceinput").removeClass("is-invalid");
    }

    let speech_input = $("#speechinput").val();
    if (speech_input.length > 300) {
        $("#speechinput").addClass("is-invalid");
        isvalid = false;
    } else {
        $("#speechinput").removeClass("is-invalid");
    }

    if (!isvalid) {
        document.getElementById("submitButton").disabled = false;
    }

    return isvalid;
}

$("#form").bind('ajax:complete', function () {
    document.getElementById("submitButton").disabled = false;
});

// Fetch all the forms we want to apply custom Bootstrap validation styles to
let initialstate = null;
let courseidglobal = null;
let lessonidglobal = null;

function fetchData(courseId, lessonNumber) {
    $.ajax({
        url: `/fetch-lesson-terms/${courseId}/${lessonNumber}`,
        method: 'GET',
        success: function (terms) {
            initialstate = terms;
            var csrf_token = $('meta[name="csrf-token"]').attr('content');
            $('#table-title').text(`ASL${courseId} Lesson ${lessonNumber}`);
            var tableBodyHTML = '';
            terms.forEach(function (term) {
                tableBodyHTML += `
                    <tr>
                        <td contenteditable="false">${term.translation}</td>
                        <td hidden>${term.cardid}</td>
                        <td contenteditable="true">${term.memorytip}</td>
                        <td contenteditable="true">${term.speech}</td>
                        <td contenteditable="true">${term.sentence}</td>
                        <td>
                            <button class="btn btn-danger remove-btn" 
                                    data-cardid="${term.cardid}" 
                                    data-csrf-token="${csrf_token}">Remove</button>
                        </td>
                    </tr>`;
            });
            $('#table-body').html(tableBodyHTML);
            $('thead').removeClass('hidden');
            $('#edit-message').show();
        },
        error: function (xhr, status, error) {
            alert("Unable to display table");
        }
    });
}

$('.lesson-link').click(function (e) {
    e.preventDefault();

    var cellsedited = document.querySelectorAll('.edited-cell');
    var cellslong = document.querySelectorAll('.too-long-input');
    if (cellsedited.length > 0 || cellslong.length > 0) {
        if (confirm('Clicking on a different lesson will cause your data to be lost. Do you want to proceed?')) {
            var courseId = $(this).data('course');
            courseidglobal = courseId;
            var lessonNumber = $(this).data('lesson');
            lessonidglobal = lessonNumber;
            fetchData(courseId, lessonNumber);
            $('#button-container').show();
        }
    } else {
        var courseId = $(this).data('course');
        courseidglobal = courseId;
        var lessonNumber = $(this).data('lesson');
        lessonidglobal = lessonNumber;
        fetchData(courseId, lessonNumber);
        $('#button-container').show();
    }
});

$(document).on("submit", "form", function (event) {
    $(window).off('beforeunload');
});

$(document).ready(function () {
    $(window).on('beforeunload', function (e) {
        var cells = document.querySelectorAll('.edited-cell');
        if (cells.length > 0) {
            return "Are you sure you want to leave? Your data will not be saved";
        }

        let speech_input = $("#speechinput").val();
        let sentence_input = $("#sentenceinput").val();
        let mem_tip = $("#memoryinput").val();
        let lesson_input = $("#lessonnumberinput").val();
        let link_input = $("#videolinkinput").val();
        let translation_input = $("#translationinput").val();

        if (speech_input.length > 0 || sentence_input.length > 0 || mem_tip.length > 0 ||
            lesson_input.length > 0 || link_input.length > 0 || translation_input.length > 0 || $("#courseinput").val() !== null) {
            return "Are you sure you want to leave? Your data will not be saved";
        }
    });

    $('#table-body').on('input', 'td[contenteditable="true"]', function () {
        $(this).addClass('edited-cell');

        var contentLength = $(this).text().trim().length;
        if (contentLength < 300) {
            $(this).removeClass('too-long-input');
        } else {
            $(this).addClass('too-long-input');
        }
    });

    $('#table-body').on('click', '.remove-btn', function () {
        var cardId = $(this).data('cardid');
        var csrf_token = $(this).data('csrf-token');

        if (confirm('Are you sure you want to permanently remove this card? This flashcard cannot be restored')) {
            var row = $(this).closest('tr');

            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrf_token);
                    }
                }
            });

            $.ajax({
                type: 'POST',
                url: '/deleteflashcard',
                data: JSON.stringify({ cardid: cardId }),
                contentType: 'application/json',
                success: function (response) {
                    row.remove();
                    for (var i = 0; i < initialstate.length; i++) {
                        if (initialstate[i].cardid === cardId)
                            initialstate.splice(i, 1);
                    }
                },
                error: function (xhr, status, error) {
                    alert("Unable to delete flashcard");
                }
            });
        } else {
            return;
        }
    });
});

$(document).ready(function () {
    function handleCellEditing() {
        $('#table-body td[contenteditable="true"]').on('input', function () {
            $(this).css('white-space', 'pre-wrap');
        });
    }

    handleCellEditing();

    $('#delete-lesson').click(function () {
        var titleText = $('#table-title').text();
        var match = titleText.match(/\d+/g);

        if (match && match.length >= 2) {
            var courseId = match[0];
            var lessonNumber = match[1];

            if (confirm('Are you sure you want to delete the entire lesson?')) {
                var csrf_token = $(this).data('csrf-token');

                $.ajaxSetup({
                    beforeSend: function (xhr, settings) {
                        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrf_token);
                        }
                    }
                });

                $.ajax({
                    type: 'POST',
                    url: '/delete-lesson',
                    data: JSON.stringify({ courseId: courseId, lessonNumber: lessonNumber }),
                    contentType: 'application/json',
                    success: function (response) {
                        location.reload();
                    },
                    error: function (xhr, status, error) {
                        alert("Unable to delete lesson");
                    }
                });
            } else {
                return;
            }
        } else {
            alert("Unable to delete lesson");
        }
    });
});

$(document).ready(function () {
    function fetchData(courseId, lessonNumber) {
        $.ajax({
            url: `/fetch-lesson-terms/${courseId}/${lessonNumber}`,
            method: 'GET',
            success: function (terms) {
                initialstate = terms;
                var courseName = $('#aslcourse option:selected').text();
                $('#table-title').text(`ASL${courseId} Lesson ${lessonNumber}`);
                generateTable(terms);
                $('thead').removeClass('hidden');
                $('#edit-message').show();
            },
            error: function (xhr, status, error) {
                alert("Unable to refresh table");
            }
        });
    }

    function generateTable(terms) {
        var csrf_token = $('meta[name="csrf-token"]').attr('content');  // Get CSRF token from meta tag
        var tableBodyHTML = '';
        terms.forEach(function (term) {
            tableBodyHTML += `
                <tr>
                    <td contenteditable="false">${term.translation}</td>
                    <td hidden>${term.cardid}</td>
                    <td contenteditable="true">${term.memorytip}</td>
                    <td contenteditable="true">${term.speech}</td>
                    <td contenteditable="true">${term.sentence}</td>
                    <td>
                        <button class="btn btn-danger remove-btn" 
                                data-cardid="${term.cardid}" 
                                data-csrf-token="${csrf_token}">Remove</button>
                    </td>
                </tr>`;
        });
        $('#table-body').html(tableBodyHTML);
    }
    

    function noautosavechanges(csrf_token) {
        // Set up CSRF token in the AJAX header
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                // Add CSRF token to request headers
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token);
                }
            }
        });
    
        var currentdata = [];
        let validdata = true;
        $('#table-body tr').each(function () {
            var cardid = $(this).find('td:eq(1)').text();
            var translation = $(this).find('td:eq(0)').text();
            var memorytip = $(this).find('td:eq(2)').text();
            var speech = $(this).find('td:eq(3)').text();
            var sentence = $(this).find('td:eq(4)').text();
    
            if (memorytip.length >= 300) {
                validdata = false;
                $(this).find('td:eq(2)').addClass('too-long-input');
            }
    
            if (speech.length >= 300) {
                validdata = false;
                $(this).find('td:eq(3)').addClass('too-long-input');
            }
    
            if (sentence.length >= 300) {
                validdata = false;
                $(this).find('td:eq(4)').addClass('too-long-input');
            }
    
            currentdata.push({
                cardid: cardid,
                translation: translation,
                memorytip: memorytip,
                speech: speech,
                sentence: sentence
            });
        });
    
        if (validdata === false) {
            setTimeout(function () {
                document.getElementById("change-lesson").disabled = false;
                alert("Red highlighted cells exceed maximum length. Please reduce input size to save changes");
    
                // Optionally, scroll to the first cell that's too long
                $('.too-long-input').first().get(0).scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 200);
            return;
        }
    
        // Send the data with the CSRF token in the header
        $.ajax({
            type: 'POST',
            url: '/savechanges',
            contentType: 'application/json',
            data: JSON.stringify(currentdata),
            success: function (response) {
                if (response.messages && response.messages.length > 0) {
                    if (response.deleted) {
                        alert("Some cards have been deleted from the database by another administrator: " + response.messages.join(", ") + ". These cards were not updated, please manually restore them using the Add function");
                    } else {
                        alert("Updated successfully");
                    }
                } else {
                    alert("Updated successfully");
                }
                var cells = document.querySelectorAll('.edited-cell');
                cells.forEach(function (cell, index) {
                    $(cell).removeClass('edited-cell');
                });
                // Reload the table after saving changes
                fetchData(courseidglobal, lessonidglobal);
                document.getElementById("change-lesson").disabled = false;
            },
            error: function alerterror(xhr, status, error) {
                document.getElementById("change-lesson").disabled = false;
                alert("An error occured please contact system administrator");
            }
        });
    }

    $("#change-lesson").click(function () {
        var csrf_token = $(this).data('csrf-token');  // Retrieve CSRF token from the button's data attribute

        // Disable the button to prevent multiple clicks
        document.getElementById("change-lesson").disabled = true;

        $.ajax({
            type: 'PUT',
            url: `/checkchanges/${courseidglobal}/${lessonidglobal}`,
            data: JSON.stringify(initialstate),
            contentType: 'application/json',
            beforeSend: function (xhr, settings) {
                // Add CSRF token to request headers
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token);
                }
            },
            success: function (request) {
                if (request.success === true) {
                    noautosavechanges(csrf_token);
                } else {
                    if (confirm(request.message)) {
                        noautosavechanges(csrf_token);
                    } else {
                        document.getElementById("change-lesson").disabled = false;
                    }
                }
            },
            error: function alerterror(xhr, status, error) {
                document.getElementById("change-lesson").disabled = false;
                alert("An error occured please contact system administrator");
            }
        });
    });
});