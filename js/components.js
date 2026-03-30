/* ============================================
   COMPONENTS.JS — Carousel, filter, testimonials
   ============================================ */

// ---- Work Portfolio Filter ----
function initWorkFilter() {
  // Collect all filter button groups (top bar + index filters)
  const topButtons = document.querySelectorAll('.work-filter__btn');
  const indexButtons = document.querySelectorAll('.work-index__filter-btn');
  const allButtons = [...topButtons, ...indexButtons];

  // Collect all filterable items (grid cards + index rows)
  const gridItems = document.querySelectorAll('.work-grid__item');
  const indexItems = document.querySelectorAll('.work-index-item');

  if (allButtons.length === 0) return;

  function applyFilter(filter) {
    // Sync active state across all button groups
    allButtons.forEach((b) => {
      if (b.dataset.filter === filter) {
        b.classList.add('active');
      } else {
        b.classList.remove('active');
      }
    });

    // Filter grid items
    gridItems.forEach((item) => {
      if (filter === 'all' || item.dataset.category?.includes(filter)) {
        item.classList.remove('is-filtered');
      } else {
        item.classList.add('is-filtered');
      }
    });

    // Filter index items
    indexItems.forEach((item) => {
      if (filter === 'all' || item.dataset.category?.includes(filter)) {
        item.classList.remove('is-filtered');
      } else {
        item.classList.add('is-filtered');
      }
    });
  }

  allButtons.forEach((btn) => {
    btn.addEventListener('click', () => applyFilter(btn.dataset.filter));
  });
}

// ---- Testimonial Carousel ----
function initTestimonialCarousel() {
  const carousel = document.querySelector('.testimonial-carousel');
  if (!carousel) return;

  const track = carousel.querySelector('.testimonial-carousel__track');
  const slides = carousel.querySelectorAll('.testimonial-carousel__slide');
  const prevBtn = carousel.querySelector('.testimonial-carousel__btn--prev');
  const nextBtn = carousel.querySelector('.testimonial-carousel__btn--next');
  const dots = carousel.querySelectorAll('.testimonial-carousel__dot');

  if (slides.length === 0) return;

  let currentSlide = 0;
  const total = slides.length;

  function goToSlide(index) {
    currentSlide = ((index % total) + total) % total;
    track.style.transform = `translateX(-${currentSlide * 100}%)`;

    dots.forEach((dot, i) => {
      dot.classList.toggle('active', i === currentSlide);
    });
  }

  if (prevBtn) prevBtn.addEventListener('click', () => goToSlide(currentSlide - 1));
  if (nextBtn) nextBtn.addEventListener('click', () => goToSlide(currentSlide + 1));

  // Auto-advance every 5s
  let autoPlay = setInterval(() => goToSlide(currentSlide + 1), 5000);

  carousel.addEventListener('mouseenter', () => clearInterval(autoPlay));
  carousel.addEventListener('mouseleave', () => {
    autoPlay = setInterval(() => goToSlide(currentSlide + 1), 5000);
  });

  // Initialize
  goToSlide(0);
}

// ---- Blog Filter ----
function initBlogFilter() {
  const buttons = document.querySelectorAll('.blog-filter__btn');
  const items = document.querySelectorAll('.blog-grid__item');

  if (buttons.length === 0) return;

  buttons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const filter = btn.dataset.filter;

      buttons.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');

      items.forEach((item) => {
        if (filter === 'all' || item.dataset.category === filter) {
          item.style.display = '';
        } else {
          item.style.display = 'none';
        }
      });
    });
  });
}

// ---- Image Gallery Carousel (Case Studies) ----
function initGalleryCarousels() {
  document.querySelectorAll('.gallery-carousel').forEach((carousel) => {
    const track = carousel.querySelector('.gallery-carousel__track');
    const slides = carousel.querySelectorAll('.gallery-carousel__slide');
    const counter = carousel.querySelector('.gallery-carousel__counter');
    const prevBtn = carousel.querySelector('.gallery-carousel__prev');
    const nextBtn = carousel.querySelector('.gallery-carousel__next');

    if (slides.length === 0) return;

    let current = 0;

    function update() {
      track.style.transform = `translateX(-${current * 100}%)`;
      if (counter) {
        counter.textContent = `${String(current + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`;
      }
    }

    if (prevBtn) prevBtn.addEventListener('click', () => {
      current = (current - 1 + slides.length) % slides.length;
      update();
    });

    if (nextBtn) nextBtn.addEventListener('click', () => {
      current = (current + 1) % slides.length;
      update();
    });

    update();
  });
}

// ---- Sticky Header ----
function initStickyHeader() {
  const stickyHeader = document.querySelector('.header-sticky');
  if (!stickyHeader) return;

  let lastScroll = 0;
  const threshold = 400;

  window.addEventListener('scroll', () => {
    const currentScroll = window.scrollY;

    if (currentScroll > threshold) {
      stickyHeader.classList.add('is-visible');
    } else {
      stickyHeader.classList.remove('is-visible');
    }

    lastScroll = currentScroll;
  });
}

// ---- Work View Toggle (Featured / Index) ----
function initViewToggle() {
  const toggle = document.getElementById('workToggle');
  if (!toggle) return;

  const opts = toggle.querySelectorAll('.work-toggle__opt');
  const featuredView = document.getElementById('featuredView');
  const indexView = document.getElementById('indexView');
  const headerPillLabel = document.getElementById('headerPillLabel');
  const pageWrapper = document.getElementById('workPageWrapper');
  const body = document.body;

  if (!featuredView || !indexView) return;

  const header = document.getElementById('workHeader');

  function switchView(view) {
    if (view === 'index') {
      featuredView.classList.remove('is-active');

      // Slide-in animation: start off-screen, then animate in
      indexView.classList.add('is-entering');
      indexView.classList.add('is-active');
      // Force reflow, then remove is-entering to trigger transition
      indexView.offsetHeight;
      indexView.classList.remove('is-entering');

      if (headerPillLabel) headerPillLabel.textContent = 'The Index';
      if (header) header.classList.add('header--index-visible');
      body.style.backgroundColor = '#0f00b0';
      body.style.color = '#ebebeb';
    } else {
      indexView.classList.remove('is-active');
      featuredView.classList.add('is-active');
      if (headerPillLabel) headerPillLabel.textContent = 'Featured Projects';
      if (header) header.classList.remove('header--index-visible');
      body.style.backgroundColor = '';
      body.style.color = '';
    }

    opts.forEach((o) => {
      o.classList.toggle('is-active', o.dataset.view === view);
    });

    // Scroll to top on view switch
    window.scrollTo({ top: 0, behavior: 'instant' });
  }

  opts.forEach((opt) => {
    opt.addEventListener('click', () => switchView(opt.dataset.view));
  });

  // Index CTA link (at bottom of featured grid)
  const indexCtaLink = document.getElementById('indexCtaLink');
  if (indexCtaLink) {
    indexCtaLink.addEventListener('click', (e) => {
      e.preventDefault();
      switchView('index');
    });
  }

  // Hash-based navigation: #index in URL auto-switches to index view
  if (window.location.hash === '#index') {
    switchView('index');
  }

  // Listen for hash changes (e.g. back/forward navigation)
  window.addEventListener('hashchange', () => {
    if (window.location.hash === '#index') {
      switchView('index');
    } else {
      switchView('featured');
    }
  });
}

// ---- Index Hover Image ----
function initIndexHover() {
  const assetsPanel = document.getElementById('indexHoverImg');
  if (!assetsPanel) return;

  const img = assetsPanel.querySelector('img');
  const items = document.querySelectorAll('.work-index-item');

  if (items.length === 0) return;

  let currentSrc = '';

  items.forEach((item) => {
    item.addEventListener('mouseenter', () => {
      const src = item.dataset.img;
      if (src && src !== currentSrc) {
        img.src = src;
        currentSrc = src;
      }
      assetsPanel.classList.add('is-visible');
    });

    item.addEventListener('mouseleave', () => {
      assetsPanel.classList.remove('is-visible');
    });
  });
}

// ---- Init ----
document.addEventListener('DOMContentLoaded', () => {
  initWorkFilter();
  initTestimonialCarousel();
  initBlogFilter();
  initGalleryCarousels();
  initStickyHeader();
  initViewToggle();
  initIndexHover();
});
