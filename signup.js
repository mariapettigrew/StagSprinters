
$(document).ready(function() {
    $("#signupBtn").on("click", function(event) {
        
        event.preventDefault();

        
        var formData = $("#signupForm").serialize();

        
        $.ajax({
            url: "/signup",
            method: "POST",
            data: formData,
            success: function(response) {
                
                if (response.success) {
                    
                    window.location.href = "/login"; 
                    
                    alert(response.message);
                }
            },
            error: function(xhr, status, error) {
                
                alert("An error occurred while signing up. Please try again later.");
                console.error(error); 
            }
        });
    });
});
