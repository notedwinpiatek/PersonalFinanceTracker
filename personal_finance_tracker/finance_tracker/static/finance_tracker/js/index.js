const currency = document.getElementById("currencyImg");
const currencySelect = document.getElementById("currencySelector");
const currencyOptions= document.querySelectorAll(".currency-option");
const url = currencySelect.dataset.url;

window.addEventListener('click', () => {
    currencySelect.style.display = 'none';
});

currency.addEventListener("click", (event) => {
    event.stopPropagation();
    if (currencySelect.style.display == 'none'){
        currencySelect.style.display = "block";
    }
    else {
        currencySelect.style.display = 'none';
    }
});

currencyOptions.forEach(option => {
    option.addEventListener("click", () => {
        const currency = option.dataset.currency;
        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({ currency })
        }).then(() => {
            location.reload();
        });
    })
})

function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    if (match) return match[2];
}