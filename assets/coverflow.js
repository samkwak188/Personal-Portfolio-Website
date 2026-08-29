/* Original Cover Flow controller — zero-reflow, index-math approach.
   The transform curve and timing intentionally match the portfolio's pre-redesign gallery. */
(function () {
  "use strict";

  function clamp(value, low, high) {
    return Math.max(low, Math.min(high, value));
  }

  function getItems(element) {
    return Array.from(element.querySelectorAll("[data-coverflow-item='true']"));
  }

  function cacheGeometry(scrollElement, items) {
    var offsets = items.map(function (item) {
      var width = item.offsetWidth;
      return {
        item: item,
        width: width,
        center: item.offsetLeft + width / 2,
        surface: item.querySelector(".coverflow-surface"),
        shadow: item.querySelector(".coverflow-shadow"),
        lastTransform: "",
        lastShadow: "",
        lastZIndex: "",
      };
    });
    return { viewportWidth: scrollElement.clientWidth, offsets: offsets };
  }

  function nearestIndex(scrollElement, geometry) {
    var viewCenter = scrollElement.scrollLeft + geometry.viewportWidth / 2;
    var bestIndex = 0;
    var bestDistance = Infinity;
    geometry.offsets.forEach(function (offset, index) {
      var distance = Math.abs(offset.center - viewCenter);
      if (distance < bestDistance) {
        bestDistance = distance;
        bestIndex = index;
      }
    });
    return bestIndex;
  }

  function attach(scrollElement) {
    var root = scrollElement.closest(".coverflow-root");
    var previousButton = root && root.querySelector(".coverflow-prev");
    var nextButton = root && root.querySelector(".coverflow-next");
    var items = getItems(scrollElement);
    if (!items.length) return { rebuild: function () {} };

    var geometry = cacheGeometry(scrollElement, items);
    var frame = null;
    var currentCenter = -1;
    var wheelLockUntil = 0;
    var dragging = false;
    var dragMoved = false;
    var pointerId = null;
    var dragStartX = 0;
    var dragStartScroll = 0;
    var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

    function loadNearbyImages(index) {
      geometry.offsets.forEach(function (offset, itemIndex) {
        if (Math.abs(itemIndex - index) > 2) return;
        offset.item.querySelectorAll("img[data-lazy-src]").forEach(function (image) {
          image.src = image.dataset.lazySrc;
          image.removeAttribute("data-lazy-src");
        });
      });
    }

    function updateCenter(index) {
      if (index === currentCenter) return;
      currentCenter = index;
      loadNearbyImages(index);
      geometry.offsets.forEach(function (offset, itemIndex) {
        var isCenter = itemIndex === index;
        var isNear = Math.abs(itemIndex - index) <= 2;
        offset.item.classList.toggle("is-center", isCenter);
        offset.item.classList.toggle("is-near", isNear);
        if (isCenter) offset.item.setAttribute("aria-current", "true");
        else offset.item.removeAttribute("aria-current");
      });
      if (previousButton) previousButton.disabled = index <= 0;
      if (nextButton) nextButton.disabled = index >= items.length - 1;
      window.__coverflowState = { centerIndex: index, itemCount: items.length };
    }

    function applyTransforms() {
      var viewCenter = scrollElement.scrollLeft + geometry.viewportWidth / 2;
      var closestIndex = 0;
      var closestDistance = Infinity;
      var edge = 0.35;

      geometry.offsets.forEach(function (offset, index) {
        var delta = offset.center - viewCenter;
        var normalized = clamp(delta / (offset.width * 1.1), -1, 1);
        var absolute = Math.abs(normalized);
        var linear = absolute <= edge ? 1 - absolute / edge : 0;
        var smooth = linear * linear * (3 - 2 * linear);
        var rotateY = (1 - smooth) * (normalized < 0 ? 15 : -15);
        var scale = 0.82 + smooth * 0.26;
        var depth = -60 + smooth * 140;
        var shift = -(1 - smooth) * normalized * 60;
        var darkness = (1 - smooth) * 0.5;
        var pixelDistance = Math.abs(delta);
        var zIndex = String(Math.round(100000 + smooth * 10000 - pixelDistance * 10) - index);
        var transform =
          "translate3d(" + Math.round(shift) + "px,0," + Math.round(depth) + "px)" +
          " rotateY(" + rotateY.toFixed(1) + "deg)" +
          " scale(" + scale.toFixed(3) + ")";
        var shadow = darkness.toFixed(2);

        if (offset.surface && offset.lastTransform !== transform) {
          offset.surface.style.transform = transform;
          offset.lastTransform = transform;
        }
        if (offset.shadow && offset.lastShadow !== shadow) {
          offset.shadow.style.opacity = shadow;
          offset.lastShadow = shadow;
        }
        if (offset.lastZIndex !== zIndex) {
          offset.item.style.zIndex = zIndex;
          offset.lastZIndex = zIndex;
        }

        if (pixelDistance < closestDistance) {
          closestDistance = pixelDistance;
          closestIndex = index;
        }
      });

      updateCenter(closestIndex);
    }

    function schedule() {
      if (frame !== null) return;
      frame = requestAnimationFrame(function () {
        frame = null;
        applyTransforms();
      });
    }

    function scrollToIndex(index, behavior) {
      var offset = geometry.offsets[index];
      if (!offset) return;
      var maximum = Math.max(0, scrollElement.scrollWidth - scrollElement.clientWidth);
      var target = clamp(offset.center - geometry.viewportWidth / 2, 0, maximum);
      scrollElement.scrollTo({
        left: target,
        behavior: reducedMotion.matches ? "auto" : (behavior || "smooth"),
      });
      schedule();
    }

    function moveBy(amount) {
      scrollToIndex(clamp(nearestIndex(scrollElement, geometry) + amount, 0, items.length - 1));
    }

    function rebuild() {
      items = getItems(scrollElement);
      geometry = cacheGeometry(scrollElement, items);
      currentCenter = -1;
      schedule();
    }

    function onWheel(event) {
      if (event.ctrlKey) return;
      var horizontal = Math.abs(event.deltaX);
      var vertical = Math.abs(event.deltaY);
      var raw = vertical >= horizontal ? event.deltaY : event.deltaX;
      if (!raw) return;

      var current = nearestIndex(scrollElement, geometry);
      var direction = raw > 0 ? 1 : -1;
      var next = clamp(current + direction, 0, items.length - 1);
      if (next === current) return;

      event.preventDefault();
      var now = performance.now();
      if (now < wheelLockUntil) return;
      scrollToIndex(next, "smooth");
      wheelLockUntil = now + 100;
    }

    function onPointerDown(event) {
      if (event.button !== 0) return;
      if (event.target.closest("a, button, input, textarea, select")) return;
      dragging = true;
      dragMoved = false;
      pointerId = event.pointerId;
      dragStartX = event.clientX;
      dragStartScroll = scrollElement.scrollLeft;
      scrollElement.style.scrollSnapType = "none";
      scrollElement.style.scrollBehavior = "auto";
      if (scrollElement.setPointerCapture) scrollElement.setPointerCapture(pointerId);
    }

    function onPointerMove(event) {
      if (!dragging || event.pointerId !== pointerId) return;
      var distance = event.clientX - dragStartX;
      if (!dragMoved && Math.abs(distance) < 5) return;
      dragMoved = true;
      event.preventDefault();
      scrollElement.scrollLeft = dragStartScroll - distance;
      schedule();
    }

    function onPointerUp(event) {
      if (!dragging || event.pointerId !== pointerId) return;
      dragging = false;
      if (scrollElement.releasePointerCapture && scrollElement.hasPointerCapture(pointerId)) {
        scrollElement.releasePointerCapture(pointerId);
      }
      pointerId = null;
      scrollElement.style.scrollSnapType = "x mandatory";
      scrollElement.style.scrollBehavior = "";
      if (dragMoved) scrollToIndex(nearestIndex(scrollElement, geometry), "smooth");
    }

    function onKeyDown(event) {
      if (event.key === "ArrowRight") {
        event.preventDefault();
        moveBy(1);
      } else if (event.key === "ArrowLeft") {
        event.preventDefault();
        moveBy(-1);
      } else if (event.key === "Home") {
        event.preventDefault();
        scrollToIndex(0);
      } else if (event.key === "End") {
        event.preventDefault();
        scrollToIndex(items.length - 1);
      }
    }

    scrollElement.addEventListener("scroll", schedule, { passive: true });
    scrollElement.addEventListener("wheel", onWheel, { passive: false });
    scrollElement.addEventListener("pointerdown", onPointerDown);
    scrollElement.addEventListener("pointermove", onPointerMove);
    scrollElement.addEventListener("pointerup", onPointerUp);
    scrollElement.addEventListener("pointercancel", onPointerUp);
    scrollElement.addEventListener("keydown", onKeyDown);
    if (previousButton) previousButton.addEventListener("click", function () { moveBy(-1); });
    if (nextButton) nextButton.addEventListener("click", function () { moveBy(1); });

    if ("ResizeObserver" in window) {
      new ResizeObserver(rebuild).observe(scrollElement);
    } else {
      window.addEventListener("resize", rebuild, { passive: true });
    }

    scrollElement.querySelectorAll("img").forEach(function (image) {
      if (!image.complete) image.addEventListener("load", rebuild, { once: true });
    });

    requestAnimationFrame(function () {
      rebuild();
      scrollToIndex(0, "auto");
      applyTransforms();
    });

    return { rebuild: rebuild, schedule: schedule };
  }

  var instances = new WeakMap();
  var initFrame = null;

  function initAll() {
    initFrame = null;
    document.querySelectorAll(".coverflow-scroll").forEach(function (element) {
      if (instances.has(element)) instances.get(element).rebuild();
      else instances.set(element, attach(element));
    });
  }

  function scheduleInit() {
    if (initFrame !== null) return;
    initFrame = requestAnimationFrame(initAll);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", scheduleInit);
  else scheduleInit();

  new MutationObserver(scheduleInit).observe(document.documentElement, {
    childList: true,
    subtree: true,
  });
})();
