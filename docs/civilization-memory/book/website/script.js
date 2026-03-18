(function () {
  var toggle = document.querySelector('.nav-toggle');
  var navList = document.querySelector('.nav-list');
  if (toggle && navList) {
    toggle.addEventListener('click', function () {
      var open = navList.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open);
    });
  }

  var sections = document.querySelectorAll('.content-section');
  function updateActiveNav() {
    if (!navList) return;
    var top = window.scrollY + 80;
    var current = null;
    sections.forEach(function (section) {
      if (section.offsetTop <= top) current = section;
    });
    if (current) {
      navList.querySelectorAll('a').forEach(function (a) {
        var id = a.getAttribute('href').slice(1);
        a.classList.toggle('active', id === current.id);
      });
    }
  }

  var progressEl = document.querySelector('.reading-progress');
  function updateProgress() {
    if (!progressEl) return;
    var doc = document.documentElement;
    var scrollable = doc.scrollHeight - window.innerHeight;
    var pct = scrollable <= 0 ? 100 : Math.min(100, Math.round((window.scrollY / scrollable) * 100));
    progressEl.style.width = pct + '%';
    progressEl.setAttribute('aria-valuenow', String(pct));
  }

  var backBtn = document.querySelector('.back-to-top');
  function updateBackToTop() {
    if (!backBtn) return;
    if (window.scrollY > 500) {
      backBtn.hidden = false;
    } else {
      backBtn.hidden = true;
    }
  }

  if (backBtn) {
    backBtn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  function onScroll() {
    updateActiveNav();
    updateProgress();
    updateBackToTop();
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('load', function () {
    updateActiveNav();
    updateProgress();
    updateBackToTop();
  });
  window.addEventListener('resize', updateProgress);

  // Close mobile nav after in-page jump
  if (navList) {
    navList.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function () {
        if (window.matchMedia('(max-width: 768px)').matches) {
          navList.classList.remove('is-open');
          if (toggle) toggle.setAttribute('aria-expanded', 'false');
        }
      });
    });
  }
})();
