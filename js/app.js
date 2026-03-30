/* ============================================
   APP.JS — Main application initialization
   Lenis smooth scroll, cursor, scrollbar, GSAP custom eases
   ============================================ */

// ---- Register Custom Eases (matching shed.design) ----
// Cubic bezier solver — converts CSS cubic-bezier values into GSAP-compatible easing functions
function cubicBezierEase(x1, y1, x2, y2) {
  // Newton-Raphson cubic bezier solver
  return function(t) {
    if (t === 0 || t === 1) return t;
    const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx;
    const cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
    function sampleX(tt) { return ((ax * tt + bx) * tt + cx) * tt; }
    function sampleY(tt) { return ((ay * tt + by) * tt + cy) * tt; }
    function sampleDerivX(tt) { return (3 * ax * tt + 2 * bx) * tt + cx; }
    // Solve for t given x using Newton's method
    let guess = t;
    for (let i = 0; i < 8; i++) {
      const err = sampleX(guess) - t;
      if (Math.abs(err) < 1e-6) break;
      const d = sampleDerivX(guess);
      if (Math.abs(d) < 1e-6) break;
      guess -= err / d;
    }
    return sampleY(guess);
  };
}

function initCustomEases() {
  if (typeof gsap === 'undefined') return;
  // Register custom eases matching the original shed.design values
  gsap.registerEase('expoIn', cubicBezierEase(0.66, 0, 0.86, 0));
  gsap.registerEase('expoOut', cubicBezierEase(0.14, 1, 0.34, 1));
  gsap.registerEase('expoInOut', cubicBezierEase(0.9, 0, 0.1, 1));
  gsap.registerEase('introOut', cubicBezierEase(0.3, 0.6, 0.9, 1));
  gsap.defaults({ ease: 'power2.out' });
}

// ---- Lenis Smooth Scroll ----
let lenis;
window.__lenis = null; // Expose globally for other scripts
function initLenis() {
  lenis = new Lenis({
    duration: 1.2,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    touchMultiplier: 2,
    infinite: false,
  });

  // Stop lenis until intro animation finishes (homepage) or page loads (inner pages)
  lenis.stop();

  function raf(time) {
    lenis.raf(time);
    requestAnimationFrame(raf);
  }
  requestAnimationFrame(raf);

  window.__lenis = lenis;

  // Connect to GSAP ScrollTrigger if available
  if (typeof ScrollTrigger !== 'undefined') {
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((time) => {
      lenis.raf(time * 1000);
    });
    gsap.ticker.lagSmoothing(0);
  }
}

// ---- Custom Cursor ----
function initCursor() {
  const cursor = document.querySelector('.cursor');
  if (!cursor || !matchMedia('(hover: hover)').matches) return;

  let cursorX = 0, cursorY = 0;
  let targetX = 0, targetY = 0;

  document.addEventListener('mousemove', (e) => {
    targetX = e.clientX;
    targetY = e.clientY;
  });

  function updateCursor() {
    cursorX += (targetX - cursorX) * 0.15;
    cursorY += (targetY - cursorY) * 0.15;
    cursor.style.transform = `translate(${cursorX}px, ${cursorY}px)`;
    requestAnimationFrame(updateCursor);
  }
  updateCursor();

  // Show/hide cursor based on hoverable elements
  document.addEventListener('mouseenter', (e) => {
    const el = e.target.closest('a, button, [data-cursor]');
    if (!el) return;
    cursor.classList.add('cursor--visible');
    const label = el.getAttribute('data-cursor') || '';
    const labelEl = cursor.querySelector('.cursor__label p');
    if (labelEl) labelEl.textContent = label;
    if (el.hasAttribute('data-cursor-small')) {
      cursor.classList.add('cursor--small');
    }
  }, true);

  document.addEventListener('mouseleave', (e) => {
    const el = e.target.closest('a, button, [data-cursor]');
    if (!el) return;
    cursor.classList.remove('cursor--visible', 'cursor--small');
  }, true);
}

// ---- Custom Scrollbar ----
function initScrollbar() {
  const scrollbar = document.querySelector('.scrollbar');
  if (!scrollbar) return;

  const handle = scrollbar.querySelector('.scrollbar__handle');
  if (!handle) return;

  function updateScrollbar() {
    const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
    if (scrollHeight <= 0) return requestAnimationFrame(updateScrollbar);
    const scrollPercent = window.scrollY / scrollHeight;
    const handleHeight = Math.max(5, (window.innerHeight / document.documentElement.scrollHeight) * 100);

    handle.style.height = handleHeight + '%';
    handle.style.top = scrollPercent * (100 - handleHeight) + '%';

    requestAnimationFrame(updateScrollbar);
  }

  updateScrollbar();
}

// ---- Mark page as loaded ----
function markPageLoaded() {
  document.body.classList.add('is-loaded');
  if (lenis) lenis.start();
  // Show scrollbar handle after intro
  const scrollbar = document.querySelector('.scrollbar');
  if (scrollbar) {
    setTimeout(() => scrollbar.classList.add('scrollbar--intro-done'), 1500);
  }
}

// ---- Init ----
document.addEventListener('DOMContentLoaded', () => {
  // Add lenis classes
  document.documentElement.classList.add('lenis', 'lenis-smooth');

  initCustomEases();
  initLenis();
  initCursor();
  initScrollbar();

  // If NOT homepage (no .home-hero), start immediately
  const hero = document.querySelector('.home-hero');
  if (!hero) {
    // Inner pages: start Lenis + scrollbar right away
    markPageLoaded();
  }
  // Homepage intro is triggered by initHomeHeroIntro() in animations.js
});
