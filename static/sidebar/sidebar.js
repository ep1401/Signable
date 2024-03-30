'use strict'


function handleclick() {

   

    

        $("#bdSidebar").toggleClass("width1", "width2")
        $(".text").toggle()
        

    
    
   
  
    
}

function handleclick2() {
    $("#bdSidebar").removeClass("width2")
    $("#bdSidebar").addClass("width1")
    $(".text").show()
}
function setup() {
    $("#hide").click(handleclick);
    $("#mobileshow").click(handleclick2)

   
}

$('document').ready(setup);