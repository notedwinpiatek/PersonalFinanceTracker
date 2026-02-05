const errorTexts = document.querySelectorAll('.error-text');
const errorWrappers = document.querySelectorAll('.error-wrapper');

document.querySelector('input[name="username"]').setAttribute('placeholder', 'Username');
document.querySelector('input[name="password"]').setAttribute('placeholder', 'Password');

// Show wrappers only if there's a relevant error
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
});

// Show all error wrappers if any error exists
if (hasVisibleError) {
    errorWrappers.forEach(wrapper => wrapper.style.display = 'flex');
}

// Hide all error wrappers if user clicks outside of any of them
document.addEventListener('click', function (event) {
    errorWrappers.forEach(wrapper => {
        if (!wrapper.contains(event.target)) {
            wrapper.style.display = 'none';
        }
    });
});
