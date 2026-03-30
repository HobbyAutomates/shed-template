/* ============================================
   ANIMATIONS.JS — Scroll triggers, text splits, reveals
   Uses GSAP ScrollTrigger + IntersectionObserver
   ============================================ */

// ---- Text Splitter ----
function splitText(el) {
  const text = el.textContent.trim();
  const type = el.classList.contains('anim-char') ? 'char' : 'word';

  if (type === 'char') {
    el.innerHTML = text.split('').map((char) =>
      char === ' '
        ? ' '
        : `<span class="char" style="display:inline-block">${char}</span>`
    ).join('');
  } else {
    el.innerHTML = text.split(/\s+/).map((word) =>
      `<span class="oh" style="display:inline-block;overflow:hidden"><span class="word" style="display:inline-block">${word}</span></span>`
    ).join(' ');
  }

  el.classList.add('text-splitter--splitted');
}

// ---- Initialize Text Splits ----
function initTextSplits() {
  document.querySelectorAll('.anim-word, .anim-char').forEach(splitText);
}

// ---- Scroll-Triggered Visibility ----
function initScrollReveals() {
  const revealElements = new Set();
  const isHomepage = !!document.querySelector('.home-hero');

  document.querySelectorAll(
    '.anim-word, .anim-char, .anim-line, .anim-fade, .clip-reveal, [data-reveal]'
  ).forEach((el) => {
    // Skip elements controlled by the homepage intro animation
    if (el.hasAttribute('data-intro-title')) return;
    revealElements.add(el);
  });

  // For inner pages (not homepage), immediately reveal elements in the initial viewport
  // with a staggered delay so they animate in sequence
  if (!isHomepage) {
    let staggerIndex = 0;
    revealElements.forEach((el) => {
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight + 50) {
        const delay = staggerIndex * 100; // 100ms stagger
        setTimeout(() => el.classList.add('is-visible'), delay);
        staggerIndex++;
      }
    });
  }

  // IntersectionObserver for elements below the fold (revealed on scroll)
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.05,
    rootMargin: '50px 0px -20px 0px'
  });

  revealElements.forEach((el) => {
    // Only observe elements that aren't already revealed
    if (!el.classList.contains('is-visible')) {
      observer.observe(el);
    }
  });
}

// ---- Section-level visibility (for parent containers) ----
function initSectionReveals() {
  const sections = document.querySelectorAll('[data-section-reveal]');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        // Also reveal children
        entry.target.querySelectorAll('[data-reveal-child]').forEach((child, i) => {
          setTimeout(() => child.classList.add('is-visible'), i * 80);
        });
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.05,
    rootMargin: '50px 0px 0px 0px'
  });

  sections.forEach((el) => observer.observe(el));
}

// ---- GSAP-powered animations (if GSAP is loaded) ----
function initGSAPAnimations() {
  if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') return;

  gsap.registerPlugin(ScrollTrigger);

  // Parallax images
  document.querySelectorAll('.parallax-wrapper').forEach((wrapper) => {
    const img = wrapper.querySelector('img');
    if (!img) return;

    gsap.to(img, {
      y: '-10%',
      ease: 'none',
      scrollTrigger: {
        trigger: wrapper.parentElement,
        start: 'top bottom',
        end: 'bottom top',
        scrub: true,
      }
    });
  });

  // Clip-path hero image reveals (project detail pages)
  document.querySelectorAll('.project-hero__fig').forEach((fig) => {
    // Trigger immediately on page load with a delay
    setTimeout(() => {
      fig.classList.add('is-visible');
    }, 600);
  });

  // Scale-in elements
  document.querySelectorAll('[data-gsap-scale]').forEach((el) => {
    gsap.from(el, {
      scale: 0,
      duration: 1,
      ease: 'elastic.out(1, 0.5)',
      scrollTrigger: {
        trigger: el,
        start: 'top 85%',
        once: true,
      }
    });
  });

  // Line draw animation for vertical rules
  document.querySelectorAll('[data-line-draw]').forEach((el) => {
    gsap.from(el, {
      scaleY: 0,
      duration: 1.2,
      ease: 'power3.out',
      transformOrigin: 'top',
      scrollTrigger: {
        trigger: el,
        start: 'top 80%',
        once: true,
      }
    });
  });
}

// ---- Home Hero Cinematic Intro Animation ----
// Replicates the original shed.design intro: hero images start zoomed/clipped to a
// small centered rectangle, then clip-path animates to reveal, and the first image
// scales down from the zoomed state to fill the full hero viewport.
function initHomeHeroIntro() {
  const hero = document.querySelector('.home-hero');
  if (!hero) return;

  const container = hero.querySelector('.home-hero-assets');
  const assetsWrapper = hero.querySelector('.home-hero-assets__wrapper');
  if (!container || !assetsWrapper) return;

  const assets = Array.from(assetsWrapper.querySelectorAll('.home-hero-asset'));
  const wrappers = Array.from(assetsWrapper.querySelectorAll('.home-hero-asset__wrapper'));
  const introRef = hero.querySelector('.home-hero-assets__intro');

  if (assets.length === 0 || wrappers.length === 0) return;

  const isDesktop = window.innerWidth >= 1024;

  // If no intro reference element or no GSAP, skip cinematic intro
  if (!introRef || typeof gsap === 'undefined') {
    assets[0].style.opacity = '1';
    hero.classList.add('home-hero--visible');
    if (typeof markPageLoaded === 'function') markPageLoaded();
    startHeroCarousel(assets);
    return;
  }

  // --- Calculate scale factor ---
  // The intro reference is a small centered box (26.5vw desktop, 70vw mobile).
  // We scale assets UP so they appear to fill only that small box initially,
  // then animate the scale back to 1 (full viewport).
  const introRect = introRef.getBoundingClientRect();
  const assetRect = assets[0].getBoundingClientRect();
  const scaleFactor = isDesktop
    ? introRect.height / assetRect.height
    : introRect.width / assetRect.width;

  // Calculate clip percentages so only the intro-sized area is visible
  const clipX = 50 - (introRect.width / (window.innerWidth * scaleFactor)) * 100 / 2;
  const clipY = 50 - (introRect.height / (assetRect.height * scaleFactor)) * 100 / 2;

  // --- Set up intro state ---
  container.classList.add('home-hero-assets--intro');
  gsap.set(assets, { opacity: 1 });
  gsap.set(wrappers, {
    scale: scaleFactor,
    '--clipX': clipX + '%',
    '--clipY': isDesktop ? '100%' : clipY + '%',
    '--clipYBot': isDesktop ? '0%' : (100 - clipY) + '%',
  });

  // --- Build GSAP intro timeline ---
  const tl = gsap.timeline({
    delay: 0.3,
    onComplete: () => {
      // Clean up: remove intro state, start scroll parallax, start carousel
      container.classList.remove('home-hero-assets--intro');
      gsap.set(assets, { clearProps: 'all' });
      gsap.set(assets[0], { opacity: 1, zIndex: 1 });
      gsap.set(wrappers, { clearProps: 'all' });
      hero.classList.add('home-hero--visible');
      if (typeof markPageLoaded === 'function') markPageLoaded();
      initHeroScrollParallax(container);
      startHeroCarousel(assets);
    }
  });

  // Step 1: Clip-path reveal — staggered across all asset wrappers
  // Use cubic-bezier fallback if CustomEase not loaded
  const easeInOut = 'expoInOut';
  const easeIntro = 'introOut';

  if (isDesktop) {
    // Desktop: clip-path opens from bottom (--clipY goes from 100% to 0%)
    tl.fromTo(wrappers,
      { '--clipY': '100%' },
      {
        '--clipX': clipX + '%',
        '--clipY': '0%',
        ease: easeInOut,
        duration: 1.2,
        stagger: { each: -0.35, ease: easeIntro }
      }, 0);
  } else {
    // Mobile: clip-path opens from top (--clipYBot decreases)
    tl.fromTo(wrappers,
      { '--clipYBot': (100 - clipY) + '%' },
      {
        '--clipYBot': clipY + '%',
        ease: easeInOut,
        duration: 1.2,
        stagger: { each: -0.35, ease: easeIntro }
      }, 0);
  }

  // Step 2: Scale the first asset wrapper back to 1 (zoom out to full viewport)
  const figScaleLabel = 0.38 + 0.35 * (wrappers.length + 1);
  tl.addLabel('figScale', figScaleLabel);
  tl.to(wrappers[0], {
    scale: 1,
    '--clipX': '0%',
    '--clipY': '0%',
    '--clipYBot': '0%',
    clearProps: 'all',
    ease: easeInOut,
    duration: 1.2,
  }, 'figScale');

  // Step 3: Reveal the hero title words
  tl.add(() => {
    const words = hero.querySelectorAll('.home-hero-title .word');
    if (words.length > 0) {
      gsap.fromTo(words,
        { yPercent: 103 },
        { yPercent: 0, duration: 1.2, stagger: 0.25, force3D: true, ease: easeInOut }
      );
    }
  }, 'figScale+=0.2');

  // Remove the intro sizing reference element (it was only needed for calculations)
  introRef.style.display = 'none';
}

// ---- Hero Scroll Parallax (after intro completes) ----
function initHeroScrollParallax(container) {
  if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') return;
  gsap.to(container, {
    yPercent: 40,
    ease: 'none',
    scrollTrigger: {
      trigger: '.home-hero',
      start: 'top top',
      end: 'bottom top',
      scrub: true,
    }
  });
}

// ---- Hero Image Carousel (after intro completes) ----
function startHeroCarousel(assets) {
  if (assets.length <= 1) return;

  let currentIndex = 0;
  let zCounter = 2;

  setInterval(() => {
    const nextIndex = (currentIndex + 1) % assets.length;

    // Prepare next asset
    gsap.set(assets[nextIndex], {
      clipPath: 'inset(0% 0% 100% 0%)',
      zIndex: zCounter++,
      opacity: 1,
    });

    // Update carousel thumbnail control
    const controlImg = document.querySelector('.home-hero-carousel-control__img');
    if (controlImg) {
      const nextImg = assets[nextIndex].querySelector('img');
      if (nextImg) controlImg.src = nextImg.src;
    }

    // Animate clip reveal
    gsap.to(assets[nextIndex], {
      clipPath: 'inset(0% 0% 0% 0%)',
      duration: 1,
      ease: 'expoInOut',
      onComplete: () => {
        // Reset previous asset
        gsap.set(assets[currentIndex], { clearProps: 'clipPath,zIndex,opacity' });
        zCounter = 2;
        currentIndex = nextIndex;
      }
    });
  }, 5000);
}

// ---- Home Services Hover ----
function initServiceHover() {
  const wrapper = document.querySelector('.home-services__list-wrapper');
  if (!wrapper) return;

  const items = wrapper.querySelectorAll('.home-service-item');
  const figsWrapper = document.querySelector('.home-services__figs-wrapper');
  const figs = document.querySelectorAll('.home-services__fig');

  if (!figsWrapper || figs.length === 0) return;

  items.forEach((item, index) => {
    item.addEventListener('mouseenter', () => {
      figsWrapper.querySelector('.home-services__figs')?.classList.add('home-services__figs--visible');
      figs.forEach((fig) => fig.classList.remove('is-active'));
      if (figs[index]) figs[index].classList.add('is-active');
    });
  });

  wrapper.addEventListener('mouseleave', () => {
    figsWrapper.querySelector('.home-services__figs')?.classList.remove('home-services__figs--visible');
    figs.forEach((fig) => fig.classList.remove('is-active'));
  });
}

// ---- Init ----
document.addEventListener('DOMContentLoaded', () => {
  initTextSplits();
  initScrollReveals();
  initSectionReveals();
  initGSAPAnimations();
  initHomeHeroIntro();
  initServiceHover();
});
