'use strict'


function handleclick() {

   

    $("#sidebar").toggleClass("sidebar-wrapper sidebar-size")
    let visible = $(".text").attr("display")
    console.log(visible)
    if (visible === "none") {
        setTimeout(() => {
            $(".text").toggle()
        }, 1000);
    
    } else {
        $(".text").toggle()
        
    }
    
    
   
  
    
}
function setup() {
    $("#button").click(handleclick);
    $("#logo-2").toggle()
}

$('document').ready(setup);