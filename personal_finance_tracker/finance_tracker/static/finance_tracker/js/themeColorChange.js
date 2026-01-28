const colorContainer = document.getElementById('colorContainer');
const colorChangeButton = document.getElementById("colorChangeBtn");
const colorBtn = document.getElementById("colorChangeBtn");
const themes = [
  { name: 'pink', secondary: '#be3eb8ff' },
  { name: 'grey', secondary: '#9b9b9bff' },
  { name: 'green', secondary: '#5aa736ff' },
  { name: 'brown', secondary: '#b46c3cff' },
  { name: 'blue', secondary: '#3e4bacff' },
  { name: 'lightBlue', secondary: '#3ea8afff' }
];

function buildColorPopup() {
  colorContainer.innerHTML = '';

  const currentTheme = document.documentElement.getAttribute('data-theme');

  themes.forEach(theme => {
    const tile = document.createElement('div');
    tile.className = 'color-tile';
    tile.style.background = theme.secondary;
    tile.dataset.theme = theme.name;

    if (theme.name === currentTheme) {
      tile.classList.add('active');
    }

    tile.addEventListener('click', () => {
      setTheme(theme.name);
      closePopup();
    });

    colorContainer.appendChild(tile);
  });
}

function togglePopup() {
  colorContainer.classList.toggle('open');
  if (colorContainer.classList.contains('open')) {
    buildColorPopup();
  }
}

function closePopup() {
  colorContainer.classList.remove('open');
}

colorBtn.addEventListener('click', (e) => {
  e.stopPropagation();
  togglePopup();
});

document.addEventListener('click', () => {
  closePopup();
});

