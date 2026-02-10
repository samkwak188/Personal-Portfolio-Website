/* Cover Flow controller — zero-reflow, index-math approach
   Inspired by github.com/addyosmani/threejs-coverflow
   and scroll-driven-animations.style/demos/cover-flow/css/ */
(function () {
  "use strict";

  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

  function getItems(el) {
    return Array.from(el.querySelectorAll("[data-coverflow-item='true']"));
  }

  /* ---- cached geometry ---- */

  function cacheGeometry(scrollEl, items) {
    // Read offsetLeft + offsetWidth once — no per-frame reflow
    var offsets = [];
    for (var i = 0; i < items.length; i++) {
      var it = items[i];
      offsets.push({
        left: it.offsetLeft,
        width: it.offsetWidth,
        center: it.offsetLeft + it.offsetWidth / 2,
        surface: it.querySelector(".coverflow-surface"),
        shadow: it.querySelector(".coverflow-shadow"),
      });
    }
    return {
      viewportW: scrollEl.clientWidth,
      offsets: offsets,
    };
  }

  /* ---- transform math (pure computation, no DOM reads) ---- */

  function applyTransforms(scrollEl, geo) {
    var viewCenter = scrollEl.scrollLeft + geo.viewportW / 2;
    var closestIdx = 0;
    var closestDist = Infinity;
    var offsets = geo.offsets;
    var EDGE = 0.35;

    for (var i = 0; i < offsets.length; i++) {
      var o = offsets[i];
      var delta = o.center - viewCenter;
      var norm = clamp(delta / (o.width * 1.1), -1, 1);
      var absN = Math.abs(norm);

      var t = absN <= EDGE ? 1 - absN / EDGE : 0;
      var s = t * t * (3 - 2 * t); // smoothstep

      var rotateY = (1 - s) * (norm < 0 ? 15 : -15);
      var scale   = 0.82 + s * 0.26;
      var zDepth  = -60 + s * 140;
      var shiftX  = -(1 - s) * norm * 60;
      var opacity = 1;
      // Ensure consistent stacking with overlap (no ties): nearer-to-center always on top
      // Use pixel distance (delta) + index tiebreaker so right side never reverses.
      var distPx = Math.abs(delta);
      var zIndex = Math.round(100000 + s * 10000 - distPx * 10) - i;

      // darkness: 0 at center, 0.5 on shelf (simulates light falloff)
      var darkness = (1 - s) * 0.5;

      if (o.surface) {
        o.surface.style.transform =
          "translate3d(" + (shiftX | 0) + "px,0," + (zDepth | 0) + "px)" +
          " rotateY(" + rotateY.toFixed(1) + "deg)" +
          " scale(" + scale.toFixed(3) + ")";
      }
      if (o.shadow) {
        o.shadow.style.opacity = darkness.toFixed(2);
      }
      // z-index on the item wrapper (not surface)
      offsets[i]._zIndex = zIndex;

      var dist = Math.abs(delta);
      if (dist < closestDist) { closestDist = dist; closestIdx = i; }
    }

    // Batch z-index + is-center writes
    for (var j = 0; j < offsets.length; j++) {
      var item = scrollEl.querySelectorAll("[data-coverflow-item='true']")[j];
      if (!item) continue;
      item.style.zIndex = offsets[j]._zIndex;
      if (j === closestIdx) {
        item.classList.add("is-center");
      } else {
        item.classList.remove("is-center");
      }
    }
  }

  /* ---- scroll-to helpers ---- */

  function scrollToIdx(scrollEl, geo, idx, behavior) {
    var o = geo.offsets[idx];
    if (!o) return;
    var target = o.center - geo.viewportW / 2;
    var max = Math.max(0, scrollEl.scrollWidth - scrollEl.clientWidth);
    scrollEl.scrollTo({ left: clamp(target, 0, max), behavior: behavior || "smooth" });
  }

  function nearestIdx(scrollEl, geo) {
    var vc = scrollEl.scrollLeft + geo.viewportW / 2;
    var best = 0, bestD = Infinity;
    for (var i = 0; i < geo.offsets.length; i++) {
      var d = Math.abs(geo.offsets[i].center - vc);
      if (d < bestD) { bestD = d; best = i; }
    }
    return best;
  }

  /* ---- attach ---- */

  function attach(scrollEl) {
    var items = getItems(scrollEl);
    if (!items.length) return { schedule: function () {} };

    var geo = cacheGeometry(scrollEl, items);
    var rafId = null;
    var wheelLockUntil = 0;

    function schedule() {
      if (rafId !== null) return;
      rafId = requestAnimationFrame(function () {
        rafId = null;
        applyTransforms(scrollEl, geo);
      });
    }

    function rebuildGeo() {
      items = getItems(scrollEl);
      geo = cacheGeometry(scrollEl, items);
      schedule();
    }

    /* wheel — snap to next/prev card */
    function onWheel(event) {
      if (event.ctrlKey) return;
      var absY = Math.abs(event.deltaY);
      var absX = Math.abs(event.deltaX);
      var raw = absY >= absX ? event.deltaY : event.deltaX;
      if (!raw) return;

      var now = performance.now();
      if (now < wheelLockUntil) { event.preventDefault(); return; }

      var dir = raw > 0 ? 1 : -1;
      var cur = nearestIdx(scrollEl, geo);
      var next = clamp(cur + dir, 0, items.length - 1);
      event.preventDefault();
      scrollToIdx(scrollEl, geo, next, "smooth");
      wheelLockUntil = now + 100;
      schedule();
    }

    /* drag / swipe */
    var isDragging = false;
    var dragStartX = 0;
    var dragScrollStart = 0;

    var dragHasMoved = false;
    var DRAG_THRESHOLD = 5;

    function onPointerDown(event) {
      if (event.button && event.button !== 0) return;
      /* Allow normal clicks on interactive elements (buttons, links) */
      var tgt = event.target;
      if (tgt && tgt.closest && tgt.closest("a, button, [role='button'], input, textarea, select")) {
        return;
      }
      isDragging = true;
      dragHasMoved = false;
      dragStartX = event.clientX != null ? event.clientX : event.touches[0].clientX;
      dragScrollStart = scrollEl.scrollLeft;
      scrollEl.style.cursor = "grabbing";
      scrollEl.style.scrollSnapType = "none";
      scrollEl.style.scrollBehavior = "auto";
      event.preventDefault();
    }

    function onPointerMove(event) {
      if (!isDragging) return;
      var x = event.clientX != null ? event.clientX : event.touches[0].clientX;
      if (!dragHasMoved && Math.abs(x - dragStartX) < DRAG_THRESHOLD) return;
      dragHasMoved = true;
      event.preventDefault();
      scrollEl.scrollLeft = dragScrollStart + (dragStartX - x);
      schedule();
    }

    function onPointerUp() {
      if (!isDragging) return;
      isDragging = false;
      scrollEl.style.cursor = "grab";
      scrollEl.style.scrollSnapType = "x mandatory";
      scrollEl.style.scrollBehavior = "";
      scrollToIdx(scrollEl, geo, nearestIdx(scrollEl, geo), "smooth");
      schedule();
    }

    scrollEl.addEventListener("mousedown", onPointerDown);
    scrollEl.addEventListener("mousemove", onPointerMove);
    window.addEventListener("mouseup", onPointerUp);
    scrollEl.addEventListener("touchstart", onPointerDown, { passive: false });
    scrollEl.addEventListener("touchmove", onPointerMove, { passive: false });
    scrollEl.addEventListener("touchend", onPointerUp);
    scrollEl.addEventListener("touchcancel", onPointerUp);
    scrollEl.style.cursor = "grab";

    scrollEl.addEventListener("scroll", schedule, { passive: true });
    scrollEl.addEventListener("wheel", onWheel, { passive: false });
    window.addEventListener("resize", rebuildGeo);

    // Initial: center first card, apply transforms
    scrollToIdx(scrollEl, geo, 0, "instant");
    applyTransforms(scrollEl, geo);
    schedule();

    return { schedule: schedule, rebuild: rebuildGeo };
  }

  /* ---- init / re-init ---- */

  var instances = new WeakMap();

  function initAll() {
    document.querySelectorAll(".coverflow-scroll").forEach(function (el) {
      if (instances.has(el)) {
        // Tab switched back — rebuild geometry (dimensions may have changed)
        instances.get(el).rebuild();
      } else {
        instances.set(el, attach(el));
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAll);
  } else {
    initAll();
  }

  var observer = new MutationObserver(function () {
    setTimeout(initAll, 60);
  });
  observer.observe(document.documentElement, { childList: true, subtree: true });
})();
