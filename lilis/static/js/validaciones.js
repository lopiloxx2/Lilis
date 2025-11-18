document.addEventListener("DOMContentLoaded", function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    const rutInput = document.getElementById("id_rut");

    // Validador de RUT (Chile) en JS
    function validarRutJS(rutRaw) {
        if (!rutRaw) return false;
        // Quitar puntos, guiones y espacios, y pasar a mayúsculas
        const rut = rutRaw.toString().toUpperCase().replace(/\./g, '').replace(/-/g, '').trim();

        // Debe terminar en dígito o K, y tener al menos 2 caracteres (cuerpo + DV)
        if (!/^\d+[0-9K]$/.test(rut)) return false;

        const cuerpo = rut.slice(0, -1);
        const dv = rut.slice(-1);

        let suma = 0;
        let multiplo = 2;
        for (let i = cuerpo.length - 1; i >= 0; i--) {
            suma += parseInt(cuerpo.charAt(i), 10) * multiplo;
            // ciclo 2,3,4,5,6,7,2,3,... (volver a 2 cuando multiplo === 7)
            multiplo = (multiplo === 7) ? 2 : multiplo + 1;
        }

        const resto = suma % 11;
        const digito = 11 - resto;
        let dvEsperado;
        if (digito === 11) dvEsperado = '0';
        else if (digito === 10) dvEsperado = 'K';
        else dvEsperado = String(digito);

        return dv === dvEsperado;
    }

    if (rutInput) {
        rutInput.addEventListener("blur", function () {
            const valor = rutInput.value;
            if (!validarRutJS(valor)) {
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

document.querySelector('form').addEventListener('submit', function(e) {
  e.preventDefault(); // evita recarga
  // lógica personalizada
});