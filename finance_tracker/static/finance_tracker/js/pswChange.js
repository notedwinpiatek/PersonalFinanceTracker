const errorTexts = document.querySelectorAll('.error-text');
const errorWrappers = document.querySelectorAll('.error-wrapper');

document.querySelector('input[name="old_password"]').setAttribute('placeholder', 'Current Password');
document.querySelector('input[name="new_password1"]').setAttribute('placeholder', 'New Password');
document.querySelector('input[name="new_password2"]').setAttribute('placeholder', 'Confirm New Password');

errorTexts.forEach(el => {
    const original = el.innerText.toLowerCase();

    if (original.includes('this field is required')) {
        el.innerText = 'This field cannot be empty.';
    }

    if (original.includes('too similar to your other personal information')) {
        el.innerText = 'Password is too similar to your name.';
    }

    if (original.includes('too short')) {
        el.innerText = 'Password must be longer.';
    }

    if (original.includes('too common')) {
        el.innerText = 'Choose a stronger password.';
    }

    if (original.includes('entirely numeric')) {
        el.innerText = 'Password cannot be only numbers.';
    }

    if (original.includes('your old password was entered incorrectly')) {
        el.innerText = 'Old password is incorrect.';
    }

    if (original.includes('the two password fields didn’t match')) {
        el.innerText = 'Passwords must match.';
    }
});

// Always show wrappers if there are any errors
errorWrappers.forEach(wrapper => {
    wrapper.style.display = 'flex';
});

// Optional: hide error when user clicks outside
document.addEventListener('click', function (event) {
    errorWrappers.forEach(wrapper => {
        if (!wrapper.contains(event.target)) {
            wrapper.style.display = 'none';
        }
    });
});
