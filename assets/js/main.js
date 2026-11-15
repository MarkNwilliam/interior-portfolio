(() => {
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".nav");

  const onScroll = () => {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 24);
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = document.body.classList.toggle("menu-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
    nav.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => {
        document.body.classList.remove("menu-open");
        toggle.setAttribute("aria-expanded", "false");
      })
    );
  }

  const reveals = document.querySelectorAll(".reveal");
  const revealVisible = () => {
    reveals.forEach((el) => {
      if (el.classList.contains("in")) return;
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight * 0.96 && rect.bottom > 0) {
        el.classList.add("in");
      }
    });
  };
  if ("IntersectionObserver" in window && reveals.length) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    reveals.forEach((el) => io.observe(el));
    window.addEventListener("load", revealVisible);
    setTimeout(revealVisible, 400);
  } else {
    reveals.forEach((el) => el.classList.add("in"));
  }

  const yearEls = document.querySelectorAll("[data-year]");
  yearEls.forEach((el) => (el.textContent = new Date().getFullYear()));

  const triggers = [...document.querySelectorAll(".lightbox-trigger")];
  if (triggers.length) {
    const box = document.createElement("div");
    box.className = "lightbox";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-modal", "true");
    box.setAttribute("aria-label", "Image viewer");
    box.innerHTML = `
      <button class="lb-close" aria-label="Close image viewer"></button>
      <button class="lb-prev" aria-label="Previous image"></button>
      <button class="lb-next" aria-label="Next image"></button>
      <figure><img alt=""><figcaption></figcaption></figure>`;
    document.body.appendChild(box);

    const img = box.querySelector("img");
    const cap = box.querySelector("figcaption");
    const icons = {
      close: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M6 6l12 12M18 6L6 18"/></svg>',
      prev: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M15 5l-7 7 7 7"/></svg>',
      next: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M9 5l7 7-7 7"/></svg>',
    };
    box.querySelector(".lb-close").innerHTML = icons.close;
    box.querySelector(".lb-prev").innerHTML = icons.prev;
    box.querySelector(".lb-next").innerHTML = icons.next;

    let index = 0;
    let lastFocus = null;

    const show = (i) => {
      index = (i + triggers.length) % triggers.length;
      const trigger = triggers[index];
      const source = trigger.querySelector("img");
      img.src = trigger.dataset.full || source.src;
      img.alt = source.alt || "";
      const figure = trigger.closest("figure");
      cap.textContent = figure?.querySelector("figcaption")?.textContent || source.alt || "";
      box.classList.add("open");
      document.body.style.overflow = "hidden";
      box.querySelector(".lb-close").focus();
    };

    const close = () => {
      box.classList.remove("open");
      document.body.style.overflow = "";
      if (lastFocus) lastFocus.focus();
    };

    triggers.forEach((trigger, i) => {
      trigger.setAttribute("tabindex", "0");
      trigger.setAttribute("role", "button");
      trigger.setAttribute("aria-label", "Open image");
      trigger.addEventListener("click", () => {
        lastFocus = trigger;
        show(i);
      });
      trigger.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          lastFocus = trigger;
          show(i);
        }
      });
    });

    box.querySelector(".lb-close").addEventListener("click", close);
    box.querySelector(".lb-prev").addEventListener("click", () => show(index - 1));
    box.querySelector(".lb-next").addEventListener("click", () => show(index + 1));
    box.addEventListener("click", (e) => {
      if (e.target === box) close();
    });
    document.addEventListener("keydown", (e) => {
      if (!box.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(index - 1);
      if (e.key === "ArrowRight") show(index + 1);
    });
  }
})();
