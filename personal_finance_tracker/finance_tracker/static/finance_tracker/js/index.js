const currency = document.getElementById("currencyImg");
const currencySelect = document.getElementById("currencySelector");

currency.addEventListener("click", () => {
    if (currencySelect.style.display == 'none'){
        currencySelect.style.display = "block";
    }
    else {
        currencySelect.style.display = 'none';
    }
})