/* ============================================
   TRANSITIONS.JS — Page transition overlay
   ============================================ */

function initPageTransitions() {
  const overlay = document.querySelector('.page-transition-overlay');
  if (!overlay) return;

  // Intercept internal navigation links
  document.querySelectorAll('a[href]').forEach((link) => {
    const href = link.getAttribute('href');

    // Skip external links, anchors, and special protocols
    if (!href || href.startsWith('#') || href.startsWith('http') ||
        href.startsWith('mailto:') || href.startsWith('tel:') ||
        link.hasAttribute('data-no-transition')) return;

    link.addEventListener('click', (e) => {
      e.preventDefault();
      const target = href;

      // Play exit animation
      overlay.style.transition = 'transform 0.5s cubic-bezier(0.43, 0.2, 0.02, 1)';
      overlay.style.transform = 'translateY(0)';

      setTimeout(() => {
        window.location.href = target;
      }, 500);
    });
  });

  // Play enter animation on page load
  window.addEventListener('pageshow', () => {
    overlay.style.transform = 'translateY(0)';
    requestAnimationFrame(() => {
      overlay.style.transition = 'transform 0.6s cubic-bezier(0.43, 0.2, 0.02, 1)';
      overlay.style.transform = 'translateY(-100%)';
    });
  });
}

document.addEventListener('DOMContentLoaded', initPageTransitions);
