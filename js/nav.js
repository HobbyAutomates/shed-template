/* ============================================
   NAV.JS — Full-screen navigation overlay
   ============================================ */

function initNav() {
  const nav = document.querySelector('.nav');
  const toggleOpen = document.querySelector('.nav-toggle--open');
  const toggleClose = document.querySelector('.nav-toggle--close');
  const overlay = document.querySelector('.transition-overlay');
  const body = document.body;

  if (!nav || !toggleOpen) return;

  function openNav() {
    nav.classList.add('is-open');
    body.classList.add('nav-open');
    if (typeof lenis !== 'undefined') lenis.stop();

    // Update toggle
    toggleOpen.style.display = 'none';
    if (toggleClose) toggleClose.style.display = 'flex';
  }

  function closeNav() {
    nav.classList.remove('is-open');
    body.classList.remove('nav-open');
    if (typeof lenis !== 'undefined') lenis.start();

    // Update toggle
    toggleOpen.style.display = 'flex';
    if (toggleClose) toggleClose.style.display = 'none';
  }

  toggleOpen.addEventListener('click', openNav);
  if (toggleClose) toggleClose.addEventListener('click', closeNav);
  if (overlay) overlay.addEventListener('click', closeNav);

  // Close on link click
  nav.querySelectorAll('.nav-item__link').forEach((link) => {
    link.addEventListener('click', () => {
      closeNav();
    });
  });

  // Close on Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && nav.classList.contains('is-open')) {
      closeNav();
    }
  });
}

document.addEventListener('DOMContentLoaded', initNav);
