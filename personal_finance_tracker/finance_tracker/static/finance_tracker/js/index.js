const currency = document.getElementById("currencyImg");
const currencySelect = document.getElementById("currencySelector");
const currencyOptions= document.querySelectorAll(".currency-option");
const trigger = document.getElementById("yearTrigger");
const yearScroll = document.getElementById("yearScroll");
const url = currencySelect.dataset.url;

window.addEventListener('click', () => {
    yearScroll.classList.remove("expanded");
    currencySelect.classList.remove("expanded");
});

currency.addEventListener("click", (event) => {
    event.stopPropagation();
    currencySelect.classList.toggle("expanded");
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

trigger.addEventListener("click", function (event) {
    event.stopPropagation();
    const activeYear = yearScroll.querySelector(".active");
    if (activeYear) {
        activeYear.scrollIntoView()
    }
    yearScroll.classList.toggle("expanded");
});

function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    if (match) return match[2];
}