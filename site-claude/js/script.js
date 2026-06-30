/* =====================================================
   BELLOSOM APARELHOS AUDITIVOS — Landing Page
   Identificação de conversão nos CTAs (orçamento / WhatsApp)
   ===================================================== */

(function () {
  "use strict";

  function pushConversionEvent(eventName, ctaLabel) {
    if (window.dataLayer && typeof window.dataLayer.push === "function") {
      window.dataLayer.push({ event: eventName, cta_label: ctaLabel || "" });
    }
  }

  document.querySelectorAll(".cta-orcamento, .cta-whatsapp").forEach(function (el) {
    el.addEventListener("click", function () {
      var eventName = el.classList.contains("cta-whatsapp") ? "whatsapp_click" : "orcamento_click";
      pushConversionEvent(eventName, el.dataset.ctaLabel);
    });
  });
})();
