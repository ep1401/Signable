'use strict'

document.getElementById("mirrorLink").addEventListener("click", function(event) {
    event.preventDefault();
    
    document.getElementById("mirrorForm").submit();
});

document.getElementById("quizLink").addEventListener("click", function(event) {
    event.preventDefault();
    
    document.getElementById("quizForm").submit();
});



function handleclick() {

   

    

        $("#bdSidebar").toggleClass("width1", "width2")
        $(".text").toggle()
        $(".logo").toggle()
        $("#hide").addClass("fa-flip")
        $("#hide").toggleClass("fa-x fa-bars")
        $("#hide").removeClass("fa-flip")
        

    
    
   
  
    
}

function handleclick2() {
    $("#hide").removeClass("fa-bars")
    $("#hide").addClass("fa-x")
    $(".logo").show()
    $("#bdSidebar").removeClass("width2")
    $("#bdSidebar").addClass("width1")
    $(".text").show()
}

function setup() {
    $("#hide").click(handleclick);
    $("#mobileshow").click(handleclick2);

   
}

$('document').ready(setup);
