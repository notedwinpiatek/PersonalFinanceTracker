function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
}

// Apply saved theme immediately
const savedTheme = localStorage.getItem('theme') || 'blue';
document.documentElement.setAttribute('data-theme', savedTheme);
