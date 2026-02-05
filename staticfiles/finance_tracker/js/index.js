const currency = document.getElementById("currencyImg");
const currencySelect = document.getElementById("currencySelector");
const currencyOptions= document.querySelectorAll(".currency-option");
const yearTrigger = document.getElementById("yearTrigger");
const yearScroll = document.getElementById("yearScroll");
const monthsTrigger = document.getElementById("monthsTrigger");
const monthsScroll = document.getElementById("monthsScroll");
const monthsDisplay = document.getElementById("monthsDisplay");
const url = currencySelect.dataset.url;

window.addEventListener('resize', updateMonthTriggerBehavior);
window.addEventListener('DOMContentLoaded', updateMonthTriggerBehavior);
window.addEventListener('click', windowClick);
if (yearTrigger) yearTrigger.addEventListener("click", yearTriggerClick);
currency.addEventListener("click", currencyClick);
currencyOptions.forEach(option => {
    option.addEventListener("click", currencyOptionClick)
})

function updateMonthTriggerBehavior() {
    if (monthsTrigger && monthsDisplay) {
        if (window.innerWidth < 1200) {
            monthsDisplay.textContent = monthsTrigger.getAttribute("data-month");
            monthsTrigger.addEventListener("click", monthTriggerClick);
        } else {
            monthsTrigger.removeEventListener("click", monthTriggerClick);
            monthsDisplay.textContent = "";
        }
    }
}

function windowClick() {
    if(yearScroll) yearScroll.classList.remove("expanded");
    currencySelect.classList.remove("expanded");
    if(yearScroll) monthsScroll.classList.remove("expanded");
}

function currencyClick(event) {
    event.stopPropagation();
    currencySelect.classList.toggle("expanded");
}

function currencyOptionClick() {
    const currency = this.dataset.currency;
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
}

function yearTriggerClick(event) {
    event.stopPropagation();
    const activeYear = yearScroll.querySelector(".active");
    if (activeYear) {
        activeYear.scrollIntoView()
    }
    yearScroll.classList.toggle("expanded");
}

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