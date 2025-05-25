const datepickerInput = document.getElementById('datepickerInput');
const dateInput = document.getElementById('dateInput');
const datepickerImg = document.getElementById('datepickerImg');
const datepickerCalendar = document.getElementById('datepickerCalendar');
const monthYearHeader = document.getElementById('monthYear');
const daysContainer = document.getElementById('days');

let mm = "", dd = "", yyyy = "", formatted = "";
let currentDate = new Date();
let today = new Date();

datepickerInput.addEventListener('input', dateFormatter);
datepickerImg.addEventListener('click', openDatePicker);
window.addEventListener('click', windowClick);

function windowClick(event) {
    if (!datepickerCalendar.contains(event.target)) {
        datepickerCalendar.classList.remove("expanded");
    }
}

function dateFormatter(event){
    let raw = event.target.value.replace(/\D/g, "");
    mm = "";
    dd = "";
    yyyy = "";
    formatted = "";

    switch (raw.length){
        case 1:
            if (raw >= 2) {
                mm = `0${raw}`;
            } else if( raw == 1 ) {
                mm = raw;
            }
            break;
        case 2:
            if (raw[0] == 1 && raw[1] <= 2 ) {
                mm = raw;
            }
            break;
        case 3:
            if (raw[2] >= 4) {
                dd = `0${raw[2]}`;
            } else if(raw[2] < 4 && raw[2] >= 1) {
                dd = raw[2]
            }
            if (raw[0] && raw[1]) mm = `${raw[0]}${raw[1]}`;
            break;
        case 4:
            if (raw[2] != 3 ||(raw[2] == 3 && raw[3] <= 1)){
                dd = `${raw[2]}${raw[3]}`
            }
            if (raw[0] && raw[1]) mm = `${raw[0]}${raw[1]}`;
            break;
        default:
            let yearInput = raw.slice(4); 
            if (raw[0] && raw[1]) mm = `${raw[0]}${raw[1]}`;
            if (raw[2] && raw[3]) dd = `${raw[2]}${raw[3]}`;

            if (yearInput.length < 4) {
                yyyy = yearInput;
            } else {
                let year = parseInt(yearInput.slice(0, 4));
                const currentYear = new Date().getFullYear();
        
                if (year < 2015) {
                    yyyy = '2015';
                } else if (year > currentYear) {
                    yyyy = currentYear.toString();
                } else {
                    yyyy = year.toString();
                }
            }
            break;
    }

    if (mm && dd && yyyy.length == 4) {
        let maxDay = 31;
        const month = parseInt(mm);
        const day = parseInt(dd);
        const year = parseInt(yyyy);

        switch(month) {
            case 4: case 6: case 9: case 11:
                maxDay = 30;
                break;
            case 2:
                maxDay = ((year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0))? 29: 28;
                break;
        }

        if (day > maxDay) {
            dd = maxDay.toString();
        }
    }

    formatted = 
    (mm && dd && yyyy)? `${mm}/${dd}/${yyyy}`:
    (mm && dd && dd == 1 || dd == 2 || dd == 3)? `${mm}/${dd}`:
    (mm && dd)? `${mm}/${dd}/`:
    (mm && mm == 1)? `${mm}`:
    (mm)? `${mm}/`: '';

    event.target.value = formatted;
    if (/^\d{2}\/\d{2}\/\d{4}$/.test(formatted)){
        dateInput.value = formatted;
        console.log(dateInput.value)
    }
}

function openDatePicker(event){
    event.stopPropagation();
    datepickerCalendar.classList.toggle("expanded");
    renderCalendar()
}

function changeMonth(delta) {
    const newMonth = currentDate.getMonth() + delta;
    const newYear = currentDate.getFullYear();
    const currentYear = new Date().getFullYear();

    if (newMonth < 0) {
        newYear -= 1;
    } else if (newMonth > 11) {
        newYear += 1;
    }

    if (newYear >= 2015 && newYear <= currentYear){
        currentDate.setMonth(newMonth);
        renderCalendar();
    }
}

function changeYear(delta) {
    const newYear = currentDate.getFullYear() + delta;
    const currentYear = new Date().getFullYear();

    if (newYear >= 2015 && newYear <= currentYear){
        currentDate.setFullYear(currentDate.getFullYear() + delta);
        renderCalendar();
    }
}

function renderCalendar() {
    monthYearHeader.textContent = currentDate.toLocaleString('default', { month: 'long', year: 'numeric' });
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();

    daysContainer.innerHTML = '';

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    
    for (let i = 0; i < firstDay; i++) {
        daysContainer.innerHTML += `<div></div>`;
    }

    for (let i = 1; i <= daysInMonth; i++) {
        daysContainer.innerHTML += `<div class="populated">${i}</div>`
    }

    highlightToday();
}

function highlightToday(){
    const day = today.getDate();
    const month = today.getMonth();
    const monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"];
    const monthName = monthNames[month];
    const year = today.getFullYear();

    if (monthYearHeader.innerText.trim() == `${monthName} ${year}`){
        const days = daysContainer.querySelectorAll('div');
        days.forEach((d) => {
            if (d.innerText == day){
                d.classList.add('today')
            }
        })
    }
}