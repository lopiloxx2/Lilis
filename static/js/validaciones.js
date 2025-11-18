document.addEventListener("DOMContentLoaded", function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    const rutInput = document.getElementById("id_rut");

    if (rutInput) {
        rutInput.addEventListener("blur", function () {
            const valor = rutInput.value.trim().toUpperCase();

            
            const regex = /^[0-9]+[0-9K]$/;

            if (!regex.test(valor)) {
                rutInput.classList.add("is-invalid");
            } else {
                rutInput.classList.remove("is-invalid");
            }
        });
    }

    // Validación de teléfono para permitir solo números
    const telInput = document.getElementById("id_telefono");
    if (telInput) {
        telInput.addEventListener("blur", function () {
            if (!/^[0-9]*$/.test(telInput.value)) {
                telInput.classList.add("is-invalid");
            } else {
                telInput.classList.remove("is-invalid");
            }
        });
    }
});
