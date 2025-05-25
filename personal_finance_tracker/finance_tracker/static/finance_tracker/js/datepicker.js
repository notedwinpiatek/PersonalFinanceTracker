const datepickerInput = document.getElementById('datepickerInput');
let mm = "", dd = "", yyyy = "", formatted = "";

datepickerInput.addEventListener('input', () => {
    let raw = datepickerInput.value.replace(/\D/g, "");
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

    datepickerInput.value = formatted;
});


function isValidDate(value) {
    const [mm, dd, yyyy] = value.split("/").map(Number);
    const date = new Date(yyyy, mm - 1, dd);
    return (
        date.getFullYear() === yyyy &&
        date.getMonth() === mm - 1 &&
        date.getDate() === dd
    );
}