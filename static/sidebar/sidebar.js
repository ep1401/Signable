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
        }
    };

}());

// Handle the sidebar functionality
function handleclick2() {
    $("#hide").removeClass("fa-bars")
    $("#hide").addClass("fa-x")
    $(".logo").show()
    $("#bdSidebar").removeClass("width2")
    $("#bdSidebar").addClass("width1")
    $(".text").show()
}

$(document).ready(function() {
    // Pass the `adminValue` from the global window to SidebarModule
    SidebarModule.init(window.adminValue);
});
