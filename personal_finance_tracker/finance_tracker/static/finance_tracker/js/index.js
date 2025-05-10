const currency = document.getElementById("currencyImg");
const currencySelect = document.getElementById("currencySelector");
const currencyOptions= document.querySelectorAll(".currency-option");
const yearTrigger = document.getElementById("yearTrigger");
const yearScroll = document.getElementById("yearScroll");
const monthsTrigger = document.getElementById("monthsTrigger");
const monthsScroll = document.getElementById("monthsScroll");
const monthsDisplay = document.getElementById("monthsDisplay");
const url = currencySelect.dataset.url;

function updateMonthTriggerBehavior() {
    if (window.innerWidth < 1200) {
        monthsDisplay.textContent = monthsTrigger.getAttribute("data-month");
        monthsTrigger.addEventListener("click", monthTriggerClick);
    } else {
        monthsTrigger.removeEventListener("click", monthTriggerClick);
        monthsDisplay.textContent = "";
    }
}

window.addEventListener('resize', updateMonthTriggerBehavior);
window.addEventListener('DOMContentLoaded', updateMonthTriggerBehavior);

window.addEventListener('click', () => {
    yearScroll.classList.remove("expanded");
    currencySelect.classList.remove("expanded");
    monthsScroll.classList.remove("expanded");
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

yearTrigger.addEventListener("click", function (event) {
    event.stopPropagation();
    const activeYear = yearScroll.querySelector(".active");
    if (activeYear) {
        activeYear.scrollIntoView()
    }
    yearScroll.classList.toggle("expanded");
});

function monthTriggerClick(event) {
    event.stopPropagation();
    const activeMonth = monthsScroll.querySelector(".active");
    if (activeMonth) {
        activeMonth.scrollIntoView()
    }
    monthsScroll.classList.toggle("expanded");
}

function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    if (match) return match[2];
}