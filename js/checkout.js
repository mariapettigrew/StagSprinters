$(document).ready(function() {
    
    function initializeTotalPrice() {
        let storedTotalPrice = localStorage.getItem("totalPrice") || "Total: $0.00";
        let numericTotalPrice = parseFloat(storedTotalPrice.replace(/[^0-9.-]+/g, ""));
        $("#foodTotal").text(storedTotalPrice);  
        $("#totalPriceInput").val(numericTotalPrice.toFixed(2));  
    }

    initializeTotalPrice();  

    
    $("#buyBtn").off().on("click", function(event) {
        event.preventDefault();  
        let updatedTotalPrice = parseFloat($("#foodTotal").text().replace(/[^0-9.-]+/g, ""));
        $("#totalPriceInput").val(updatedTotalPrice.toFixed(2));  
        this.form.submit();  
    });


    document.querySelectorAll('.payment-option').forEach(option => {
        option.addEventListener('change', togglePaymentDetails);
    });

    function togglePaymentDetails() {
        const paymentForm = document.getElementById('paymentForm');
        const checkoutForm = document.getElementById('checkoutForm');
        paymentForm.style.display = (document.getElementById('debitCard').checked) ? 'block' : 'none';
        checkoutForm.style.height = (document.getElementById('debitCard').checked) ? '140vh' : '110vh';
    }
});
