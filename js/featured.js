const navToggle = document.getElementById('nav-toggle');
const navLinks = document.querySelector('.nav-menu');
const scrollLinks = document.querySelectorAll('.nav-item');
const closeBtn = document.getElementById('close-btn');

navToggle.addEventListener('click', () => {
  navLinks.classList.add('show-links');
  closeBtn.classList.remove('hidden');
});

function removeActive() {
  scrollLinks.forEach((link) => {
    link.classList.remove('active');
  });
}

scrollLinks.forEach((link) => {
  link.addEventListener('click', (e) => {
    navLinks.classList.remove('show-links');
    removeActive();
    e.target.classList.add('active');
  });
});

closeBtn.addEventListener('click', () => {
  navLinks.classList.remove('show-links');
  closeBtn.classList.add('hidden');
});


function countDown() {
  const now = new Date();
  const eventDate = new Date(2023, 5, 18, 4);
  const currentTime = now.getTime();
  const eventTime = eventDate.getTime();

  const remTime = eventTime - currentTime;
  let s = Math.floor(remTime / 1000);
  let m = Math.floor(s / 60);
  let h = Math.floor(m / 60);
  const d = Math.floor(h / 24);

  h %= 24;
  m %= 60;
  s %= 60;

  h = h < 10 ? `0${h}` : h;
  m = m < 10 ? `0${m}` : m;
  s = s < 10 ? `0${s}` : s;
  document.getElementById('days').textContent = d;
  document.getElementById('hours').textContent = h;
  document.getElementById('minutes').textContent = m;
  document.getElementById('seconds').textContent = s;

  setTimeout(countDown, 1000);
}
countDown();