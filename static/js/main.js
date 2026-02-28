/* ====================================================
   main.js — ObesityAI Client-Side Logic
   - Dark/Light theme toggle with localStorage persistence
   - Live BMI calculation
   - Modal open/close
   - Scroll reveal animations
   - Nav active state
   ==================================================== */

/* ------------------------------------
   1. THEME TOGGLE
   ------------------------------------ */
(function () {
  const body = document.getElementById('app-body');
  const btn = document.getElementById('theme-toggle');
  const icon = document.getElementById('theme-icon');
  const PREF_KEY = 'oa-theme';

  function applyTheme(theme) {
    if (theme === 'light') {
      body.classList.add('light-theme');
      if (icon) icon.textContent = '☀️';
    } else {
      body.classList.remove('light-theme');
      if (icon) icon.textContent = '🌙';
    }
  }

  // Load saved preference
  const saved = localStorage.getItem(PREF_KEY) || 'dark';
  applyTheme(saved);

  // Toggle on button click
  if (btn) {
    btn.addEventListener('click', function () {
      const isLight = body.classList.contains('light-theme');
      const next = isLight ? 'dark' : 'light';
      applyTheme(next);
      localStorage.setItem(PREF_KEY, next);
      // Notify charts to re-draw with new colors
      document.dispatchEvent(new CustomEvent('themechange', { detail: { theme: next } }));
    });
  }
})();

/* ------------------------------------
   1b. HAMBURGER MENU (mobile nav)
   ------------------------------------ */
(function () {
  var hamburger = document.getElementById('nav-hamburger');
  var navLinks = document.getElementById('nav-links');

  if (!hamburger || !navLinks) return;

  // Toggle open/close
  hamburger.addEventListener('click', function (e) {
    e.stopPropagation();
    hamburger.classList.toggle('open');
    navLinks.classList.toggle('open');
  });

  // Close when any nav link is clicked
  navLinks.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', function () {
      hamburger.classList.remove('open');
      navLinks.classList.remove('open');
    });
  });

  // Close when clicking outside the navbar
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.navbar')) {
      hamburger.classList.remove('open');
      navLinks.classList.remove('open');
    }
  });
})();

/* ------------------------------------
   2. NAVIGATION ACTIVE STATE
   ------------------------------------ */
(function () {
  const path = window.location.pathname;
  const navHome = document.getElementById('nav-home');
  const navPredict = document.getElementById('nav-predict');
  const navStats = document.getElementById('nav-stats');

  if (navHome) navHome.classList.remove('active');
  if (navPredict) navPredict.classList.remove('active');
  if (navStats) navStats.classList.remove('active');
  var navEducate = document.getElementById('nav-educate');
  if (navEducate) navEducate.classList.remove('active');

  if (path === '/' && navHome) navHome.classList.add('active');
  else if (path.startsWith('/predict') && navPredict) navPredict.classList.add('active');
  else if (path.startsWith('/statistics') && navStats) navStats.classList.add('active');
  else if (path.startsWith('/educate') && navEducate) navEducate.classList.add('active');
})();

/* ------------------------------------
   3. LIVE BMI CALCULATION
   ------------------------------------ */
(function () {
  const heightInput = document.getElementById('height');
  const weightInput = document.getElementById('weight');
  const bmiDisplay = document.getElementById('bmi-display');
  const bmiValue = document.getElementById('bmi-value');
  const bmiBadge = document.getElementById('bmi-badge');

  if (!heightInput || !weightInput) return;

  function calcBMI() {
    const h = parseFloat(heightInput.value);
    const w = parseFloat(weightInput.value);
    if (!h || !w || h < 50 || w < 10) {
      if (bmiDisplay) bmiDisplay.style.display = 'none';
      return;
    }

    const bmi = w / ((h / 100) ** 2);
    const rounded = bmi.toFixed(1);

    if (bmiValue) bmiValue.textContent = rounded;
    if (bmiDisplay) bmiDisplay.style.display = 'flex';

    if (bmiBadge) {
      if (bmi < 18.5) {
        bmiBadge.textContent = 'Underweight';
        bmiBadge.className = 'bmi-badge bmi-underweight';
      } else if (bmi < 25) {
        bmiBadge.textContent = 'Normal';
        bmiBadge.className = 'bmi-badge bmi-normal';
      } else if (bmi < 30) {
        bmiBadge.textContent = 'Overweight';
        bmiBadge.className = 'bmi-badge bmi-overweight';
      } else {
        bmiBadge.textContent = 'Obese';
        bmiBadge.className = 'bmi-badge bmi-obese';
      }
    }
  }

  heightInput.addEventListener('input', calcBMI);
  weightInput.addEventListener('input', calcBMI);
  calcBMI(); // Run once on load if values are pre-filled
})();

/* ------------------------------------
   4. NUTRITION MODAL
   ------------------------------------ */
function openModal() {
  var overlay = document.getElementById('nutrition-modal');
  if (!overlay) return;
  overlay.classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  var overlay = document.getElementById('nutrition-modal');
  if (!overlay) return;
  overlay.classList.remove('active');
  document.body.style.overflow = '';
}

(function () {
  var overlay = document.getElementById('nutrition-modal');
  if (!overlay) return;

  // Close on backdrop click
  overlay.addEventListener('click', function (e) {
    if (e.target === overlay) closeModal();
  });

  // Close on Escape key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeModal();
  });
})();

/* ------------------------------------
   DOWNLOAD REPORT
   Submits the hidden form to /download-report
   Flask returns a CSV file for the browser to download
   ------------------------------------ */
function downloadReport() {
  var form = document.getElementById('download-form');
  if (form) {
    form.submit();
  } else {
    alert('No prediction data found. Please submit the form first.');
  }
}

/* ------------------------------------
   5. CONFIDENCE BAR ANIMATION
   ------------------------------------ */
(function () {
  var fill = document.querySelector('.confidence-fill');
  if (!fill) return;
  var pct = fill.getAttribute('data-pct') || '0';
  requestAnimationFrame(function () {
    setTimeout(function () {
      fill.style.width = pct + '%';
    }, 200);
  });
})();

/* ------------------------------------
   6. SCROLL REVEAL ANIMATIONS
   ------------------------------------ */
(function () {
  if (!('IntersectionObserver' in window)) return;

  var items = document.querySelectorAll('.reveal');
  if (!items.length) return;

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  items.forEach(function (el) { observer.observe(el); });
})();

/* ------------------------------------
   7. COUNTER ANIMATION (Hero stats)
   ------------------------------------ */
(function () {
  var counters = document.querySelectorAll('.count-up');
  if (!counters.length) return;

  function animateCounter(el) {
    var rawTarget = parseInt(el.getAttribute('data-target'), 10);
    var suffix = el.getAttribute('data-suffix') || '';
    var divide = parseInt(el.getAttribute('data-divide'), 10) || 1;

    // Fallback legacy decimal detection if divide is not set
    if (divide === 1 && suffix === '%' && rawTarget > 100) {
      divide = 10;
    }

    var displayTarget = rawTarget / divide;
    var duration = 1600;
    var step = displayTarget / (duration / 16);
    var current = 0;

    el.textContent = '0' + suffix;

    var timer = setInterval(function () {
      current += step;
      if (current >= displayTarget) {
        current = displayTarget;
        clearInterval(timer);
      }
      if (divide > 1) {
        el.textContent = current.toFixed(1) + suffix;
      } else {
        el.textContent = Math.floor(current).toLocaleString() + suffix;
      }
    }, 16);
  }

  if ('IntersectionObserver' in window) {
    var counterObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          counterObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    counters.forEach(function (el) { counterObserver.observe(el); });
  } else {
    counters.forEach(animateCounter);
  }
})();

/* ------------------------------------
   SCROLL TO TOP BUTTON
   Shows after scrolling 300px, smooth-scrolls back to top on click
   ------------------------------------ */
const initScrollBtn = () => {
  const btn = document.getElementById('scroll-top-btn');
  if (!btn) return;

  const handleScroll = () => {
    const scrollPos = window.pageYOffset || document.documentElement.scrollTop;
    if (scrollPos > 300) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });

  btn.addEventListener('click', function () {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  handleScroll();
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initScrollBtn);
} else {
  initScrollBtn();
}
