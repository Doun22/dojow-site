/**
 * DOJOW · JavaScript principal (main.js)
 * Vanilla JS uniquement · Sections 5.5, 6.1, 9.3 et 10 de SPEC.md
 */

(function () {
  "use strict";

  /* ==========================================================================
     Utilitaires & Stockage sécurisé (try / catch)
     ========================================================================== */
  const Storage = {
    setSession(key, value) {
      try {
        sessionStorage.setItem(key, value);
      } catch (e) {
        console.warn("sessionStorage non disponible", e);
      }
    },
    getSession(key) {
      try {
        return sessionStorage.getItem(key);
      } catch (e) {
        return null;
      }
    },
    removeSession(key) {
      try {
        sessionStorage.removeItem(key);
      } catch (e) {
        console.warn("sessionStorage non disponible", e);
      }
    },
    setLocal(key, value) {
      try {
        localStorage.setItem(key, JSON.stringify(value));
      } catch (e) {
        console.warn("localStorage non disponible", e);
      }
    },
    getLocal(key) {
      try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : null;
      } catch (e) {
        return null;
      }
    }
  };

  /* ==========================================================================
     6.1 Menu mobile
     ========================================================================== */
  function initMobileMenu() {
    const burgerBtn = document.querySelector('[data-action="toggle-menu"]');
    const closeBtn = document.querySelector('[data-action="close-menu"]');
    const menuMobile = document.getElementById("menu-mobile");

    if (!burgerBtn || !menuMobile) return;

    function openMenu() {
      menuMobile.classList.add("is-open");
      burgerBtn.setAttribute("aria-expanded", "true");
      document.body.style.overflow = "hidden";
      if (closeBtn) closeBtn.focus();
    }

    function closeMenu() {
      menuMobile.classList.remove("is-open");
      burgerBtn.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
      burgerBtn.focus();
    }

    burgerBtn.addEventListener("click", function () {
      const isOpen = menuMobile.classList.contains("is-open");
      if (isOpen) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    if (closeBtn) {
      closeBtn.addEventListener("click", closeMenu);
    }

    // Fermeture avec la touche Échap
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menuMobile.classList.contains("is-open")) {
        closeMenu();
      }
    });

    // Fermeture au clic sur un lien interne du menu mobile
    const menuLinks = menuMobile.querySelectorAll("a");
    menuLinks.forEach(function (link) {
      link.addEventListener("click", function () {
        closeMenu();
      });
    });
  }

  /* ==========================================================================
     5.5 Barre d'action collante sur mobile (< 768 px)
     ========================================================================== */
  function initStickyMobileBar() {
    const stickyBar = document.getElementById("sticky-mobile-bar");
    const hero = document.getElementById("hero") || document.querySelector(".hero");
    const contactForm = document.getElementById("form-visite");

    if (!stickyBar) return;

    let heroVisible = true;
    let formVisible = false;

    function updateStickyVisibility() {
      // Visible uniquement si écran < 768px, hero hors champ, et formulaire hors champ
      if (window.innerWidth < 768 && !heroVisible && !formVisible) {
        stickyBar.classList.add("is-visible");
        stickyBar.classList.remove("is-hidden");
      } else {
        stickyBar.classList.remove("is-visible");
        stickyBar.classList.add("is-hidden");
      }
    }

    if (hero && "IntersectionObserver" in window) {
      const heroObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          heroVisible = entry.isIntersecting;
          updateStickyVisibility();
        });
      }, { threshold: 0.1 });
      heroObserver.observe(hero);
    } else {
      // Fallback si pas de hero ou pas d'observer
      heroVisible = false;
      updateStickyVisibility();
    }

    if (contactForm && "IntersectionObserver" in window) {
      const formObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          formVisible = entry.isIntersecting;
          updateStickyVisibility();
        });
      }, { threshold: 0.1 });
      formObserver.observe(contactForm);
    }

    window.addEventListener("resize", updateStickyVisibility);
  }

  /* ==========================================================================
     9.3 UTM & gclid (Capture et pré-remplissage)
     ========================================================================== */
  function initUtmAndGclid() {
    const params = new URLSearchParams(window.location.search);
    const trackingKeys = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "gclid"];

    trackingKeys.forEach(function (key) {
      const val = params.get(key);
      if (val) {
        Storage.setSession(key, val);
      }
    });

    const form = document.getElementById("form-visite");
    if (!form) return;

    trackingKeys.forEach(function (key) {
      const input = form.querySelector(`input[name="${key}"]`);
      if (input) {
        const storedVal = Storage.getSession(key);
        if (storedVal) {
          input.value = storedVal;
        }
      }
    });
  }

  /* ==========================================================================
     9.3 Validation du formulaire & mémorisation du prénom
     ========================================================================== */
  function initFormValidation() {
    const form = document.getElementById("form-visite");
    if (!form) return;

    const prenomInput = form.querySelector('input[name="prenom"]');
    const telInput = form.querySelector('input[name="telephone"]');
    const emailInput = form.querySelector('input[name="email"]');
    const submitBtn = form.querySelector('button[type="submit"]');

    function showError(input, errorElement, message) {
      if (!errorElement) return;
      errorElement.textContent = message;
      errorElement.classList.add("is-visible");
      if (input) {
        input.classList.add("is-invalid");
        input.setAttribute("aria-invalid", "true");
      }
    }

    function clearError(input, errorElement) {
      if (!errorElement) return;
      errorElement.textContent = "";
      errorElement.classList.remove("is-visible");
      if (input) {
        input.classList.remove("is-invalid");
        input.removeAttribute("aria-invalid");
      }
    }

    function validatePhone(phoneStr) {
      if (!phoneStr) return false;
      // Retire les espaces, points, tirets, parenthèses et l'indicatif +33
      let clean = phoneStr.replace(/\s+/g, "").replace(/\./g, "").replace(/-/g, "").replace(/\(/g, "").replace(/\)/g, "");
      if (clean.startsWith("+33")) {
        clean = "0" + clean.slice(3);
      }
      if (clean.startsWith("0033")) {
        clean = "0" + clean.slice(4);
      }
      const digitsOnly = clean.replace(/\D/g, "");
      return digitsOnly.length >= 10;
    }

    function validateEmail(emailStr) {
      if (!emailStr) return false;
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(emailStr);
    }

    form.addEventListener("submit", function (e) {
      let isValid = true;

      // 1. Prénom
      const errPrenom = document.getElementById("err-prenom");
      if (prenomInput) {
        if (!prenomInput.value.trim()) {
          showError(prenomInput, errPrenom, "Ce champ est requis.");
          isValid = false;
        } else {
          clearError(prenomInput, errPrenom);
        }
      }

      // 2. Téléphone
      const errTel = document.getElementById("err-telephone");
      if (telInput) {
        if (!telInput.value.trim()) {
          showError(telInput, errTel, "Ce champ est requis.");
          isValid = false;
        } else if (!validatePhone(telInput.value)) {
          showError(telInput, errTel, "Vérifiez votre numéro de téléphone.");
          isValid = false;
        } else {
          clearError(telInput, errTel);
        }
      }

      // 3. Email
      const errEmail = document.getElementById("err-email");
      if (emailInput) {
        if (!emailInput.value.trim()) {
          showError(emailInput, errEmail, "Ce champ est requis.");
          isValid = false;
        } else if (!validateEmail(emailInput.value.trim())) {
          showError(emailInput, errEmail, "Vérifiez votre adresse email.");
          isValid = false;
        } else {
          clearError(emailInput, errEmail);
        }
      }

      if (!isValid) {
        e.preventDefault();
        const firstInvalid = form.querySelector(".is-invalid");
        if (firstInvalid) {
          firstInvalid.focus();
        }
        return false;
      }

      // Si le formulaire est valide, mémorisation du prénom pour la page /merci
      if (prenomInput && prenomInput.value.trim()) {
        Storage.setSession("dojow_prenom", prenomInput.value.trim());
      }

      // État de chargement sur le bouton
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.dataset.originalText = submitBtn.textContent;
        submitBtn.textContent = "Envoi en cours...";
      }

      // Sans fetch (très vieux navigateur) : POST classique, redirection vers /merci
      if (!window.fetch || !window.FormData) return true;

      // Envoi en arrière-plan, puis fenêtre de remerciement sur la page
      e.preventDefault();
      const status = document.getElementById("form-status");
      if (status) {
        status.textContent = "";
        status.classList.remove("is-visible");
      }
      const prenom = prenomInput ? prenomInput.value.trim() : "";

      fetch(form.action, {
        method: "POST",
        headers: { Accept: "application/json" },
        body: new FormData(form)
      })
        .then(function (response) {
          return response.json().then(function (data) {
            if (!response.ok || !data.success) throw new Error(data.message || "Échec de l'envoi");
          });
        })
        .then(function () {
          Storage.removeSession("dojow_prenom");
          form.reset();
          initUtmAndGclid();
          trackConversion();
          openMerciDialog(prenom);
        })
        .catch(function () {
          if (status) {
            status.textContent = "L'envoi n'a pas fonctionné. Réessayez, ou appelez le 06 32 71 14 24.";
            status.classList.add("is-visible");
          }
        })
        .then(function () {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = submitBtn.dataset.originalText || "Réserver ma visite";
          }
        });
      return false;
    });

    // Retour arrière depuis /merci (cache du navigateur) : réactiver le bouton
    window.addEventListener("pageshow", function () {
      if (submitBtn && submitBtn.disabled) {
        submitBtn.disabled = false;
        submitBtn.textContent = submitBtn.dataset.originalText || "Réserver ma visite";
      }
    });

    // Nettoyage des erreurs à la saisie
    if (prenomInput) {
      prenomInput.addEventListener("input", function () {
        clearError(prenomInput, document.getElementById("err-prenom"));
      });
    }
    if (telInput) {
      telInput.addEventListener("input", function () {
        clearError(telInput, document.getElementById("err-telephone"));
      });
    }
    if (emailInput) {
      emailInput.addEventListener("input", function () {
        clearError(emailInput, document.getElementById("err-email"));
      });
    }
  }

  /* ==========================================================================
     Fenêtre de remerciement après envoi du formulaire (texte de SPEC 8.8)
     ========================================================================== */
  function openMerciDialog(prenom) {
    const dialog = document.getElementById("merci-dialog");
    if (!dialog || typeof dialog.showModal !== "function") {
      window.location.href = "/merci";
      return;
    }
    const title = document.getElementById("merci-dialog-titre");
    // Sécurité XSS : textContent uniquement, jamais innerHTML
    if (title) title.textContent = prenom ? `C'est noté, ${prenom} !` : "C'est noté !";
    dialog.showModal();
  }

  function initMerciDialog() {
    const dialog = document.getElementById("merci-dialog");
    if (!dialog) return;
    dialog.querySelectorAll('[data-action="close-merci"]').forEach(function (btn) {
      btn.addEventListener("click", function () {
        dialog.close();
      });
    });
    // Clic sur le fond sombre : fermeture
    dialog.addEventListener("click", function (e) {
      if (e.target === dialog) dialog.close();
    });
  }

  /* ==========================================================================
     9.3 Affichage sécurisé du prénom sur /merci
     ========================================================================== */
  function initMerciPage() {
    const merciTitle = document.getElementById("merci-titre");
    if (!merciTitle) return;

    const prenom = Storage.getSession("dojow_prenom");
    if (prenom && prenom.trim() !== "") {
      // Sécurité XSS : textContent uniquement, jamais innerHTML
      merciTitle.textContent = `C'est noté, ${prenom.trim()} !`;
      Storage.removeSession("dojow_prenom");
    } else {
      merciTitle.textContent = "C'est noté !";
    }
  }

  /* ==========================================================================
     10. Tracking et consentement (Bandeau Cookies & Google Ads)
     ========================================================================== */
  const COOKIE_CONSENT_KEY = "dojow_cookie_consent";
  const SIX_MONTHS_MS = 180 * 24 * 60 * 60 * 1000;
  // [À COMPLÉTER : ID Google Ads réel, ex. AW-123456789]
  const GOOGLE_ADS_ID = "AW-XXXXXXXXX";

  function loadGoogleAds() {
    if (window._googleAdsLoaded) return;
    window._googleAdsLoaded = true;

    // Injection asynchrone du tag gtag.js uniquement après accord
    const script = document.createElement("script");
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${GOOGLE_ADS_ID}`;
    document.head.appendChild(script);

    window.dataLayer = window.dataLayer || [];
    function gtag() {
      window.dataLayer.push(arguments);
    }
    window.gtag = gtag;

    gtag("consent", "default", {
      ad_storage: "granted",
      ad_user_data: "granted",
      ad_personalization: "granted",
      analytics_storage: "granted"
    });
    gtag("js", new Date());
    gtag("config", GOOGLE_ADS_ID);

    // Si on est sur /merci, déclenchement de la conversion principale
    if (window.location.pathname.includes("merci") || document.getElementById("merci-titre")) {
      trackConversion();
    }
  }

  // Conversion principale : page /merci, ou fenêtre de remerciement après envoi
  function trackConversion() {
    const stored = Storage.getLocal(COOKIE_CONSENT_KEY);
    if (!stored || stored.choice !== "granted" || typeof window.gtag !== "function") return;
    // [À COMPLÉTER : libellé de conversion, ex. AW-XXXXXXXXX/LIBELLE]
    window.gtag("event", "conversion", {
      send_to: `${GOOGLE_ADS_ID}/CONVERSION_LABEL`
    });
  }

  function initCookieBanner() {
    const banner = document.getElementById("cookie-banner");
    const acceptBtn = document.getElementById("cookie-accept");
    const denyBtn = document.getElementById("cookie-deny");
    const manageLinks = document.querySelectorAll('[data-action="manage-cookies"]');

    function checkConsent() {
      const stored = Storage.getLocal(COOKIE_CONSENT_KEY);
      if (!stored) {
        if (banner) banner.classList.add("is-visible");
        return;
      }

      const now = Date.now();
      if (now - stored.timestamp > SIX_MONTHS_MS) {
        // Expiré après 6 mois
        if (banner) banner.classList.add("is-visible");
        return;
      }

      if (stored.choice === "granted") {
        loadGoogleAds();
      }
    }

    if (acceptBtn) {
      acceptBtn.addEventListener("click", function () {
        Storage.setLocal(COOKIE_CONSENT_KEY, {
          choice: "granted",
          timestamp: Date.now()
        });
        if (banner) banner.classList.remove("is-visible");
        loadGoogleAds();
      });
    }

    if (denyBtn) {
      denyBtn.addEventListener("click", function () {
        Storage.setLocal(COOKIE_CONSENT_KEY, {
          choice: "denied",
          timestamp: Date.now()
        });
        if (banner) banner.classList.remove("is-visible");
        // Changement d'avis via « Gérer les cookies » : on coupe la balise déjà chargée
        if (typeof window.gtag === "function") {
          window.gtag("consent", "update", {
            ad_storage: "denied",
            ad_user_data: "denied",
            ad_personalization: "denied",
            analytics_storage: "denied"
          });
        }
      });
    }

    manageLinks.forEach(function (link) {
      link.addEventListener("click", function (e) {
        e.preventDefault();
        if (banner) {
          banner.classList.add("is-visible");
          if (acceptBtn) acceptBtn.focus();
        }
      });
    });

    checkConsent();
  }

  /* ==========================================================================
     Conversion secondaire : clics sur liens téléphoniques (tel:)
     ========================================================================== */
  function initCallTracking() {
    const telLinks = document.querySelectorAll('a[href^="tel:"]');
    telLinks.forEach(function (link) {
      link.addEventListener("click", function () {
        const stored = Storage.getLocal(COOKIE_CONSENT_KEY);
        if (stored && stored.choice === "granted" && typeof window.gtag === "function") {
          window.gtag("event", "click_call");
        }
      });
    });
  }

  /* ==========================================================================
     Boutons « Réserver ma visite » : descente jusqu'au formulaire s'il est
     sur la page (sinon, lien normal vers /#visite, le formulaire de l'accueil)
     ========================================================================== */
  function initCtaToForm() {
    const target = document.getElementById("visite");
    const form = document.getElementById("form-visite");
    if (!target || !form) return;

    const ctaLinks = document.querySelectorAll('a[href="/#visite"], a[href="#visite"], a[href="/contact-espace-coworking"]');
    ctaLinks.forEach(function (link) {
      link.addEventListener("click", function (e) {
        e.preventDefault();
        target.scrollIntoView({ block: "start" });
        const firstField = form.querySelector('input:not([type="hidden"]):not([name="botcheck"])');
        if (firstField) firstField.focus({ preventScroll: true });
      });
    });
  }

  /* ==========================================================================
     Année courante dynamique dans le footer
     ========================================================================== */
  function initDynamicYear() {
    const yearElements = document.querySelectorAll("[data-year]");
    const currentYear = new Date().getFullYear();
    yearElements.forEach(function (el) {
      el.textContent = currentYear;
    });
  }

  /* ==========================================================================
     Initialisation au chargement du DOM
     ========================================================================== */
  document.addEventListener("DOMContentLoaded", function () {
    initMobileMenu();
    initStickyMobileBar();
    initUtmAndGclid();
    initFormValidation();
    initMerciPage();
    initCookieBanner();
    initCallTracking();
    initCtaToForm();
    initMerciDialog();
    initDynamicYear();
  });
})();
