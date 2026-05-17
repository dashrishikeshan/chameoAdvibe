const contactForm = document.querySelector(".contact-form");
const menuToggle = document.querySelector(".menu-toggle");
const pageLoader = document.querySelector(".page-loader");

if (pageLoader) {
  window.addEventListener("load", () => {
    window.setTimeout(() => {
      pageLoader.classList.add("is-hidden");
    }, 450);
  });
}

if (menuToggle) {
  menuToggle.addEventListener("click", () => {
    const isOpen = document.body.classList.toggle("nav-open");
    menuToggle.setAttribute("aria-expanded", String(isOpen));
    menuToggle.setAttribute("aria-label", isOpen ? "Close menu" : "Open menu");
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 1060 && document.body.classList.contains("nav-open")) {
      document.body.classList.remove("nav-open");
      menuToggle.setAttribute("aria-expanded", "false");
      menuToggle.setAttribute("aria-label", "Open menu");
    }
  });
}

if (contactForm) {
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const status = contactForm.querySelector(".form-status");

    if (status) {
      status.textContent = "Thanks. Your enquiry is ready for the Chameo team.";
    }
  });
}

const animatedItems = document.querySelectorAll(".animate-on-scroll");

if (animatedItems.length && "IntersectionObserver" in window) {
  document.body.classList.add("effects-ready");

  const observer = new IntersectionObserver(
    (entries, activeObserver) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          activeObserver.unobserve(entry.target);
        }
      });
    },
    {
      root: null,
      rootMargin: "0px 0px -8% 0px",
      threshold: 0.12,
    },
  );

  animatedItems.forEach((item) => observer.observe(item));
}
