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
