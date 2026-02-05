const datepickerInput = document.getElementById('datepickerInput');
const dateInput = document.getElementById('dateInput');
const datepickerImg = document.getElementById('datepickerImg');
const datepickerCalendar = document.getElementById('datepickerCalendar');
const monthYearHeader = document.getElementById('monthYear');
const daysContainer = document.getElementById('days');
const todayBtn = document.getElementById('todayBtn');

let mm = "", dd = "", yyyy = "", formatted = "";
let currentDate = new Date();
let today = new Date();
let selectedDate = null;

datepickerInput.addEventListener('input', dateFormatter);
datepickerImg.addEventListener('click', openDatePicker);
todayBtn.addEventListener('click', pickToday);

window.addEventListener('click', windowClick);
window.addEventListener('keypress', windowClick);

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
            } else if( raw >= 0 ) {
                mm = raw;
            }
            break;
        case 2:
            if ((raw[0] == 1 && raw[1] <= 2) || (raw[0] == 0 && raw[1] >= 1)) {
                mm = raw;
            }
            break;
        case 3:
            if (raw[2] >= 4) {
                dd = `0${raw[2]}`;
            } else if(raw[2] < 4 && raw[2] >= 0) {
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
    (mm && dd && dd <= 1 || dd == 2 || dd == 3)? `${mm}/${dd}`:
    (mm && dd)? `${mm}/${dd}/`:
    (mm && mm <= 1)? `${mm}`:
    (mm)? `${mm}/`: '';

    event.target.value = formatted;
    if (/^\d{2}\/\d{2}\/\d{4}$/.test(formatted)){
        dateInput.value = formatted;
    }
}

function openDatePicker(event){
    event.stopPropagation();
    datepickerCalendar.classList.toggle("expanded");
    renderCalendar()
}

function changeMonth(delta) {
    let newMonth = currentDate.getMonth() + delta;
    let newYear = currentDate.getFullYear();
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

    console.log(selectedDate)

    for (let i = 1; i <= daysInMonth; i++) {
        const isSelected =
            selectedDate &&
            selectedDate.day === i &&
            selectedDate.month === month &&
            selectedDate.year === year;

        const isToday =
            i === today.getDate() &&
            month === today.getMonth() &&
            year === today.getFullYear();

        let classList = 'populated';
        if (isSelected) {
            classList += ' selectedDate';
        } else if (isToday) {
            classList += ' today';
        }

        daysContainer.innerHTML += `<div class="${classList}">${i}</div>`;
    }

    const days = daysContainer.querySelectorAll('div');
    days.forEach((day) => {
        if (day.textContent != "") {
            day.addEventListener('click', datePick)
        }
    });

}

function setDaysColor(dayInput) {
    const dayToday = today.getDate().toString();

    Array.from(daysContainer.getElementsByTagName("div")).forEach(div => {
        const text = div.textContent;

        if (text == dayToday && text != dayInput) {
            div.classList.add('today');
            div.classList.remove('selectedDate');
        } else if (text === dayInput) {
            div.classList.add('selectedDate');
            div.classList.remove('today');
        } else {
            div.classList.remove('selectedDate');
        }
    });
}

function pickToday(){
    let day = String(today.getDate());
    let month = String(today.getMonth() + 1);
    const year = today.getFullYear();

    if (day.length == 1){
        day = `0${day}`
    }
    if (month.length == 1){
        month = `0${month}`
    }

    selectedDate = { day: parseInt(day), month: parseInt(month) - 1, year: year };

    setDaysColor(day);

    const value = `${month}/${day}/${year}`
    datepickerInput.value = value;
    if (/^\d{2}\/\d{2}\/\d{4}$/.test(value)){
        dateInput.value = value;
    }
    datepickerCalendar.classList.remove('expanded');
}

function datePick(event) {
    let month = String(currentDate.getMonth() + 1);
    const year = currentDate.getFullYear();
    let day = event.target.textContent;

    selectedDate = { day: parseInt(day), month: parseInt(month) - 1, year: year };
    
    if (day.length == 1){
        day = `0${day}`
    }
    if (month.length == 1){
        month = `0${month}`
    }

    const value = `${month}/${day}/${year}`
    datepickerInput.value = value;
    if (/^\d{2}\/\d{2}\/\d{4}$/.test(value)){
        dateInput.value = value;
    }

    setDaysColor(day);

    datepickerCalendar.classList.remove('expanded');
}