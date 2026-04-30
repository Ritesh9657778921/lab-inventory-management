document.addEventListener('DOMContentLoaded', function() {
    const chemicalForm = document.getElementById('chemical-form');
    const quantityInput = document.getElementById('quantity');
    const expiryDateInput = document.getElementById('expiry_date');
    const alertContainer = document.getElementById('alert-container');

    if (chemicalForm && quantityInput && expiryDateInput && alertContainer) {
        chemicalForm.addEventListener('submit', function(event) {
            let valid = true;
            alertContainer.innerHTML = '';

            if (parseFloat(quantityInput.value) <= 0) {
                valid = false;
                alertContainer.innerHTML += '<div class="flash flash-error">Quantity must be greater than zero.</div>';
            }

            const expiryDate = new Date(expiryDateInput.value);
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            if (!expiryDateInput.value || expiryDate < today) {
                valid = false;
                alertContainer.innerHTML += '<div class="flash flash-error">Expiry date must be today or later.</div>';
            }

            if (!valid) {
                event.preventDefault();
            }
        });
    }
});