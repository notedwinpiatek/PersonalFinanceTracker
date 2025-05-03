const errorTexts = document.querySelectorAll('.error-text');
const errorWrapper = document.getElementById('errorWrapper');

document.querySelector('input[name="username"]').setAttribute('placeholder', 'Username');
document.querySelector('input[name="password"]').setAttribute('placeholder', 'Password');

// Show wrapper only if there's any relevant error
let hasVisibleError = false;

errorTexts.forEach(el => {
    const original = el.innerText.toLowerCase();

    if (original.includes('please enter a correct username and password')) {
        el.innerText = 'Wrong username or password.';
        hasVisibleError = true;
    }

    if (original.includes('this account is inactive')) {
        el.innerText = 'Your account is inactive. Please contact support.';
        hasVisibleError = true;
    }

    if (original.includes('this field is required')) {
        el.innerText = 'This field cannot be empty.';
        hasVisibleError = true;
    }

    el.classList.add('custom-error-animation');
});

// Display error wrapper only if there's something to show
if (hasVisibleError) {
    errorWrapper.style.display = 'flex';
}


document.addEventListener('click', function (event) {
    if (!errorWrapper.contains(event.target)) {
        errorWrapper.style.display = 'none';
    }
});