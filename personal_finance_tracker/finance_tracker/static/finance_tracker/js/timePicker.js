const timepickerInput = document.getElementById('timepickerInput');
const timeInput = document.getElementById('timeInput');
let h = "", m = "", amPm = "", formattedT = "";

timepickerInput.addEventListener('input', timeFormatter)

function timeFormatter(event){
    let raw = event.target.value;
    if (raw.length <= 5){
        raw = raw.replace(/\D/g, "");
    }
    h = "";
    m = "";
    amPm = "";
    formattedT = "";

    switch (raw.length){
        case 1:
            if (raw >= 2) {
                h = `0${raw}`;
            } else if( raw >= 0 ) {
                h = raw;
            }
            break;
        case 2:
            if ((raw[0] == 1 && raw[1] <= 2) || (raw[0] == 0 && raw[1] >= 1)) {
                h = raw;
            }
            break;
        case 3:
            if (raw[2] >= 6) {
                m = `0${raw[2]}`;
            } else if(raw[2] < 6 && raw[2] >= 0) {
                m = raw[2]
            }
            if (raw[0] && raw[1]) h = `${raw[0]}${raw[1]}`;
            break;
        case 4:
            m = `${raw[2]}${raw[3]}`
            if (raw[0] && raw[1]) h = `${raw[0]}${raw[1]}`;
            break;
        default:
            if (raw[0] && raw[1]) h = `${raw[0]}${raw[1]}`;
            if (raw[3] && raw[4]) m = `${raw[3]}${raw[4]}`;
            if (/[a1]/i.test(raw.slice(6))){
                amPm = "AM";
            }if (/[p2]/i.test(raw.slice(6))){
                amPm = "PM";
            }
            break;
    }

    formattedT = 
    (h && m && amPm)? `${h}:${m} ${amPm}`:
    (h && m && m.length==1)? `${h}:${m}`:
    (h && m)? `${h}:${m} `:
    (h && h <= 1)? `${h}`:
    (h)? `${h}:`: '';

    event.target.value = formattedT;
    if (/^\d{2}\:\d{2} (AM|PM)$/.test(formattedT)){
        djangoFormated = formatAmPmToDjangoTime(formattedT);
        timeInput.value = djangoFormated;
    }
}

function formatAmPmToDjangoTime(timeStr) {
    timeStr = timeStr.trim().toUpperCase();
  
    const date = new Date(`1970-01-01 ${timeStr}`);

    if (isNaN(date.getTime())) {
      console.warn("Invalid time:", timeStr);
      return null;
    }
  
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
  
    return `${hours}:${minutes}`; 
  }