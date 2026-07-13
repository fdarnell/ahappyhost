/* A Happy Host — shared script: nav toggle, carousels, contact form */

/* TODO: paste your form endpoint here (e.g. https://formspree.io/f/XXXXXXXX).
   Until it is set, the form falls back to opening the visitor's email app
   with the message pre-filled, addressed to services@ahappyhostgsm.com. */
var FORM_ENDPOINT = "";

document.addEventListener("DOMContentLoaded", function () {
  // Mobile nav toggle
  var toggle = document.querySelector(".nav-toggle");
  var menu = document.querySelector(".mainnav-inner");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Carousels: scroll-snap track + dots
  document.querySelectorAll(".carousel").forEach(function (root) {
    var track = root.querySelector(".carousel-track");
    var slides = track.querySelectorAll("img");
    var dots = root.querySelector(".carousel-dots");
    if (!dots || slides.length < 2) return;
    slides.forEach(function (_, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.setAttribute("aria-label", "Go to slide " + (i + 1));
      if (i === 0) b.setAttribute("aria-current", "true");
      b.addEventListener("click", function () {
        track.scrollTo({ left: track.clientWidth * i, behavior: "smooth" });
      });
      dots.appendChild(b);
    });
    track.addEventListener("scroll", function () {
      var i = Math.round(track.scrollLeft / track.clientWidth);
      dots.querySelectorAll("button").forEach(function (b, j) {
        if (j === i) b.setAttribute("aria-current", "true");
        else b.removeAttribute("aria-current");
      });
    }, { passive: true });
  });

  // Contact form
  var form = document.querySelector(".contact-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = form.querySelector(".form-status.ok");
      var err = form.querySelector(".form-status.err");
      ok.style.display = "none";
      err.style.display = "none";
      var data = new FormData(form);
      if (!FORM_ENDPOINT) {
        var body = "Name: " + data.get("name") + "\nEmail: " + data.get("email") +
          "\nPhone: " + data.get("phone") + "\n\n" + data.get("message");
        window.location.href = "mailto:services@ahappyhostgsm.com" +
          "?subject=" + encodeURIComponent("Website inquiry from " + data.get("name")) +
          "&body=" + encodeURIComponent(body);
        return;
      }
      fetch(FORM_ENDPOINT, {
        method: "POST",
        body: data,
        headers: { Accept: "application/json" }
      }).then(function (r) {
        if (r.ok) { ok.style.display = "block"; form.reset(); }
        else { err.style.display = "block"; }
      }).catch(function () { err.style.display = "block"; });
    });
  }
});
