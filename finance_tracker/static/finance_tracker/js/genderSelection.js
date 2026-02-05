document.querySelectorAll('.gender-options label').forEach(label => {
    label.addEventListener('click', () => {
        // Submit the form when an image is clicked
        document.getElementById('gender-form').submit();
    });
});