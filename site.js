const toggle = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
if (toggle && navigation) {
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('is-open', open);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      toggle.setAttribute('aria-expanded', 'false');
      navigation.classList.remove('is-open');
      toggle.focus();
    }
  });
}
// Keep bookmarks to sections of the previous personal homepage useful.
if (window.location.pathname === '/') {
  const destinations = { '#about': '/about/', '#teaching': '/about/#teaching', '#education': '/about/#education', '#affiliation': '/about/#affiliation', '#service': '/about/#service' };
  const destination = destinations[window.location.hash];
  if (destination) window.location.replace(destination);
}

// Load silent looping demonstrations when they enter the viewport.
const demoVideos = Array.from(document.querySelectorAll('.demo-media video'));
const visibleDemos = new Set();
function playDemo(video) {
  video.muted = true;
  if (!video.getAttribute('src')) video.src = video.dataset.src;
  if (!document.hidden) video.play().catch(() => {});
}
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(({target, isIntersecting}) => {
      if (isIntersecting) { visibleDemos.add(target); playDemo(target); }
      else { visibleDemos.delete(target); target.pause(); }
    });
  }, {threshold: 0});
  demoVideos.forEach((video) => observer.observe(video));
} else {
  demoVideos.forEach((video) => { visibleDemos.add(video); playDemo(video); });
}
document.addEventListener('visibilitychange', () => {
  demoVideos.forEach((video) => {
    if (document.hidden) video.pause();
    else if (visibleDemos.has(video)) playDemo(video);
  });
});
// Retry after a gesture if the browser initially blocks automatic playback.
document.addEventListener('pointerdown', () => visibleDemos.forEach(playDemo), {passive: true});

// Each arrow moves one photo; the track also supports touch and keyboard navigation.
const momentsTrack = document.querySelector('.moments-track');
if (momentsTrack) {
  const previous = document.querySelector('.moments-prev');
  const next = document.querySelector('.moments-next');
  function syncMoments() {
    previous.disabled = momentsTrack.scrollLeft <= 2;
    next.disabled = momentsTrack.scrollLeft >= momentsTrack.scrollWidth - momentsTrack.clientWidth - 2;
  }
  function stepMoments(direction) {
    const cards = Array.from(momentsTrack.children);
    const origin = momentsTrack.getBoundingClientRect().left;
    const positions = cards.map(card => card.getBoundingClientRect().left - origin + momentsTrack.scrollLeft);
    const current = momentsTrack.scrollLeft;
    const target = direction > 0 ? positions.find(position => position > current + 3) : positions.reverse().find(position => position < current - 3);
    momentsTrack.scrollTo({left: target === undefined ? (direction > 0 ? momentsTrack.scrollWidth : 0) : target, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
  }
  previous.addEventListener('click', () => stepMoments(-1));
  next.addEventListener('click', () => stepMoments(1));
  momentsTrack.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault(); stepMoments(event.key === 'ArrowRight' ? 1 : -1);
    }
  });
  momentsTrack.addEventListener('scroll', syncMoments, {passive:true});
  window.addEventListener('resize', syncMoments);
  momentsTrack.querySelectorAll('img').forEach(image => image.addEventListener('load', syncMoments));
  if ('ResizeObserver' in window) new ResizeObserver(syncMoments).observe(momentsTrack);
  syncMoments();
}

// Optional, one-click PERL confetti surprise. No navigation or persistent overlay.
const perlButton = document.querySelector('.perl-easter-egg');
const perlSurprise = document.querySelector('.perl-surprise');
if (perlButton && perlSurprise) {
  let hidePerlTimer;
  perlButton.addEventListener('click', () => {
    window.clearTimeout(hidePerlTimer);
    perlSurprise.textContent = 'PERL Is All You Need!';
    perlSurprise.classList.add('is-visible');
    hidePerlTimer = window.setTimeout(() => perlSurprise.classList.remove('is-visible'), 2400);
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const bounds = perlButton.getBoundingClientRect();
    const x = bounds.left + bounds.width / 2;
    const y = bounds.top + bounds.height / 2;
    const colors = ['#2f7d57', '#72bc95', '#e4bf63', '#93a9d8', '#e9a4b3'];
    for (let i = 0; i < 36; i++) {
      const particle = document.createElement('span');
      particle.className = 'perl-confetti';
      const angle = 2 * Math.PI * i / 36 + (Math.random() - .5) * .35;
      const distance = 55 + Math.random() * 125;
      particle.style.left = x + 'px';
      particle.style.top = y + 'px';
      particle.style.backgroundColor = colors[i % colors.length];
      particle.style.setProperty('--dx', Math.cos(angle) * distance + 'px');
      particle.style.setProperty('--dy', Math.sin(angle) * distance + 55 + 'px');
      particle.style.setProperty('--rot', Math.round(Math.random() * 900 - 450) + 'deg');
      particle.addEventListener('animationend', () => particle.remove(), {once:true});
      document.body.appendChild(particle);
    }
  });
}
