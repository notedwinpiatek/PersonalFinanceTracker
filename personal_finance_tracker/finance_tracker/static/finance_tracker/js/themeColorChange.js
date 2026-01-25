const colorContainer = document.getElementById('colorContainer');
const colorChangeButton = document.getElementById("colorChangeBtn");
const colorBtn = document.getElementById("colorChangeBtn");
const themes = [
  { name: 'pink', secondary: '#883584ff' },
  { name: 'grey', secondary: '#757575ff' },
  { name: 'green', secondary: '#467530ff' },
  { name: 'brown', secondary: '#7c5033ff' },
  { name: 'blue', secondary: '#30397aff' },
  { name: 'lightBlue', secondary: '#307074ff' }
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

