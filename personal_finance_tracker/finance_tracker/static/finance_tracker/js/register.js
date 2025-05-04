const errorTexts = document.querySelectorAll('.error-text');
const errorWrappers = document.querySelectorAll('.error-wrapper');


document.querySelector('input[name="username"]').setAttribute('placeholder', 'Username');
document.querySelector('input[name="password1"]').setAttribute('placeholder', 'Password');
document.querySelector('input[name="password2"]').setAttribute('placeholder', 'Confirm Password');

errorTexts.forEach(el => {
    const original = el.innerText.toLowerCase();

    if (original.includes('this field is required')) {
        el.innerText = 'This field cannot be empty.';
    }

    if (original.includes('password is too common')) {
        el.innerText = 'Choose a stronger password.';
    }

    if (original.includes("didn't match")) {
        el.innerText = 'Passwords must match.';
    }

    if (original.includes('a user with that username already exists')) {
        el.innerText = 'That username is already taken.';
    }
});

// Always show errors if they exist
errorWrappers.forEach(wrapper => {
    wrapper.style.display = 'flex';
});

document.addEventListener('click', function (event) {
    errorWrappers.forEach(wrapper => {
        if (!wrapper.contains(event.target)) {
            wrapper.style.display = 'none';
        }
    });
});