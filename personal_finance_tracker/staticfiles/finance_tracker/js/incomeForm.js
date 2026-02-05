const errorFields = document.querySelectorAll(".error-input");
const input = document.querySelector('input[type="number"]');

errorFields.forEach(field => {
    field.style.border = "2px solid red";
    field.addEventListener("input", function () {
        field.style.border = "";
    });
});

input.addEventListener('keydown', (e) => {
    if (['e', 'E', '+', '-'].includes(e.key)) {
        e.preventDefault();
    }
});