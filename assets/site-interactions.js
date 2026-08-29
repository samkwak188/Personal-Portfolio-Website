/* Navigation behavior kept outside Dash callbacks so scrolling stays native. */
(function () {
  "use strict";

  function initNavigation() {
    var header = document.querySelector(".site-header");
    var toggle = document.getElementById("menu-toggle");
    var navigation = document.getElementById("primary-navigation");
    if (!header || !toggle || !navigation) return false;
    if (header.dataset.navigationReady === "true") return true;

    header.dataset.navigationReady = "true";
    var links = Array.from(navigation.querySelectorAll("a[href^='#']"));
    var scrollFrame = null;

    function setMenu(open) {
      document.body.classList.toggle("menu-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? "Close" : "Menu";
    }

    function updateHeader() {
      scrollFrame = null;
      header.classList.toggle("is-scrolled", window.scrollY > 24);
    }

    toggle.addEventListener("click", function () {
      setMenu(toggle.getAttribute("aria-expanded") !== "true");
    });

    links.forEach(function (link) {
      link.addEventListener("click", function () { setMenu(false); });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        setMenu(false);
        toggle.focus();
      }
    });

    window.addEventListener("scroll", function () {
      if (scrollFrame !== null) return;
      scrollFrame = requestAnimationFrame(updateHeader);
    }, { passive: true });

    window.addEventListener("resize", function () {
      if (window.innerWidth > 780) setMenu(false);
    }, { passive: true });

    if ("IntersectionObserver" in window) {
      var sections = links.map(function (link) {
        return document.querySelector(link.getAttribute("href"));
      }).filter(Boolean);
      var visible = new Map();

      function updateActiveLink() {
        var activeId = null;
        var bestRatio = 0;
        visible.forEach(function (ratio, id) {
          if (ratio > bestRatio) {
            bestRatio = ratio;
            activeId = id;
          }
        });
        links.forEach(function (link) {
          var isActive = activeId && link.getAttribute("href") === "#" + activeId;
          link.classList.toggle("is-active", Boolean(isActive));
          if (isActive) link.setAttribute("aria-current", "location");
          else link.removeAttribute("aria-current");
        });
      }

      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) visible.set(entry.target.id, entry.intersectionRatio);
          else visible.delete(entry.target.id);
        });
        updateActiveLink();
      }, { rootMargin: "-18% 0px -55%", threshold: [0.08, 0.2, 0.4, 0.65] });

      sections.forEach(function (section) { observer.observe(section); });
    }

    updateHeader();
    return true;
  }

  function initSkills() {
    var instrument = document.querySelector("[data-skills-instrument='true']");
    if (!instrument) return false;
    if (instrument.dataset.skillsReady === "true") return true;

    var controls = Array.from(instrument.querySelectorAll("[data-skill-control]"));
    var panels = Array.from(instrument.querySelectorAll("[data-skill-panel]"));
    var stage = instrument.querySelector("[data-skill-stage='true']");
    if (!controls.length || !panels.length || !stage) return false;

    instrument.dataset.skillsReady = "true";
    var activeIndex = Math.max(0, controls.findIndex(function (control) {
      return control.classList.contains("is-active");
    }));

    function select(index, moveFocus) {
      activeIndex = (index + controls.length) % controls.length;
      var key = controls[activeIndex].dataset.skillControl;

      controls.forEach(function (control, controlIndex) {
        var selected = controlIndex === activeIndex;
        control.classList.toggle("is-active", selected);
        control.setAttribute("aria-selected", selected ? "true" : "false");
        control.tabIndex = selected ? 0 : -1;
      });

      panels.forEach(function (panel) {
        var selected = panel.dataset.skillPanel === key;
        panel.classList.toggle("is-active", selected);
        panel.setAttribute("aria-hidden", selected ? "false" : "true");
      });

      stage.dataset.activeSkill = key;
      if (moveFocus) controls[activeIndex].focus();
    }

    controls.forEach(function (control, index) {
      control.addEventListener("click", function () { select(index, false); });
      control.addEventListener("keydown", function (event) {
        if (event.key === "ArrowDown" || event.key === "ArrowRight") {
          event.preventDefault();
          select(activeIndex + 1, true);
        } else if (event.key === "ArrowUp" || event.key === "ArrowLeft") {
          event.preventDefault();
          select(activeIndex - 1, true);
        } else if (event.key === "Home") {
          event.preventDefault();
          select(0, true);
        } else if (event.key === "End") {
          event.preventDefault();
          select(controls.length - 1, true);
        }
      });
    });

    var finePointer = window.matchMedia("(pointer: fine)").matches;
    var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var tiltFrame = null;
    var targetTilt = [0, 0];

    function applyTilt() {
      tiltFrame = null;
      stage.style.setProperty("--skill-tilt-x", targetTilt[0].toFixed(2) + "deg");
      stage.style.setProperty("--skill-tilt-y", targetTilt[1].toFixed(2) + "deg");
    }

    if (finePointer && !reducedMotion) {
      stage.addEventListener("pointermove", function (event) {
        var rect = stage.getBoundingClientRect();
        targetTilt[0] = ((event.clientY - rect.top) / rect.height - 0.5) * -1.6;
        targetTilt[1] = ((event.clientX - rect.left) / rect.width - 0.5) * 1.8;
        if (tiltFrame === null) tiltFrame = requestAnimationFrame(applyTilt);
      }, { passive: true });
      stage.addEventListener("pointerleave", function () {
        targetTilt[0] = 0;
        targetTilt[1] = 0;
        if (tiltFrame === null) tiltFrame = requestAnimationFrame(applyTilt);
      }, { passive: true });
    }

    select(activeIndex, false);
    return true;
  }

  function boot() {
    if (initNavigation() && initSkills()) return;
    var observer = new MutationObserver(function () {
      if (initNavigation() && initSkills()) observer.disconnect();
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
