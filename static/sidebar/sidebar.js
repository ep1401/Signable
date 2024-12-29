'use strict';

var SidebarModule = SidebarModule || (function() {
    var _adminValue = ''; // Private variable to store the admin value

    return {
        // Initialize the SidebarModule with the admin value
        init: function(adminValue) {
            _adminValue = adminValue;
            console.log("Admin value from SidebarModule:", _adminValue);  // Debugging log

            this.setup();
        },

        setup: function() {
            var adminButton = document.getElementById("adminButton");
            var adminButton2 = document.getElementById("adminButton2");

            if (_adminValue !== "true") {
                console.log("Hiding admin buttons"); // Debugging log
                if (adminButton) adminButton.style.display = "none";  // Hide the first admin button
                if (adminButton2) adminButton2.style.display = "none";  // Hide the second admin button
            } else {
                console.log("Showing admin buttons"); // Debugging log
                if (adminButton) adminButton.style.display = "block";  // Show the first admin button
                if (adminButton2) adminButton2.style.display = "block";  // Show the second admin button
            }

            // Make sure handleclick2 is still available for the mobile click event
            this.bindSidebarToggle();
        },

        bindSidebarToggle: function() {
            // Ensure that the mobile sidebar toggle can still work
            $("#mobileshow").click(handleclick2);
        }
    };

}());

// The existing functions to handle sidebar toggle
function handleclick() {
    $("#bdSidebar").toggleClass("width1", "width2");
    $("#textwrapper").toggleClass("textwidth1", "textwidth2");
    $(".text").toggle();
    $(".logo").toggle();
    $("#hide").addClass("fa-flip");
    $("#hide").toggleClass("fa-x fa-bars");
    $("#hide").removeClass("fa-flip");
}

function handleclick2() {
    $("#hide").removeClass("fa-bars");
    $("#hide").addClass("fa-x");
    $(".logo").show();
    $("#bdSidebar").removeClass("width2");
    $("#bdSidebar").addClass("width1");
    $(".text").show();
}

function setup() {
    // Sidebar toggle on the desktop version
    $("#hide").click(handleclick);

    // Mobile sidebar toggle handled separately with the logic in the SidebarModule
    SidebarModule.init(window.adminValue);
}

$('document').ready(setup);
