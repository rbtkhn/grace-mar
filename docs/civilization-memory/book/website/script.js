(function () {
  var toggle = document.querySelector('.nav-toggle');
  var navList = document.querySelector('.nav-list');
  if (!toggle || !navList) return;

  toggle.addEventListener('click', function () {
    var open = navList.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', open);
  });

  // Mark current section in nav on scroll
  var sections = document.querySelectorAll('.content-section');
  function updateActive() {
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
  window.addEventListener('scroll', updateActive);
  window.addEventListener('load', updateActive);
})();
