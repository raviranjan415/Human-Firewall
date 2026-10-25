/* CyberQuest front-end toolkit.
   Small, dependency-free helpers used by the interactive pages.
   All security-relevant decisions are made on the server. */
(function () {
  "use strict";

  const csrfMeta = document.querySelector('meta[name="csrf-token"]');
  const csrfToken = csrfMeta ? csrfMeta.getAttribute("content") : "";

  async function post(url, data) {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
        "X-Requested-With": "XMLHttpRequest",
      },
      credentials: "same-origin",
      body: JSON.stringify(data || {}),
    });
    let body = null;
    try {
      body = await response.json();
    } catch (error) {
      body = { error: "unreadable_response" };
    }
    return { ok: response.ok, status: response.status, body };
  }

  function toast(message, kind) {
    let host = document.querySelector(".cq-toast-host");
    if (!host) {
      host = document.createElement("div");
      host.className = "cq-toast-host";
      host.setAttribute("role", "status");
      host.setAttribute("aria-live", "polite");
      document.body.appendChild(host);
    }
    const node = document.createElement("div");
    node.className = "cq-toast";
    if (kind === "success") node.style.borderColor = "rgba(34,197,94,.6)";
    if (kind === "error") node.style.borderColor = "rgba(239,68,68,.6)";
    node.textContent = message;
    host.appendChild(node);
    window.setTimeout(function () { node.remove(); }, 4200);
  }

  function readJson(node) {
    if (!node) return null;
    try {
      return JSON.parse(node.textContent);
    } catch (error) {
      return null;
    }
  }

  function animateBars() {
    document.querySelectorAll("[data-cq-value]").forEach(function (bar) {
      const value = Math.max(0, Math.min(100, parseFloat(bar.getAttribute("data-cq-value")) || 0));
      bar.style.width = value + "%";
    });
  }

  function autoDismissAlerts() {
    document.querySelectorAll("[data-cq-autodismiss]").forEach(function (alert) {
      window.setTimeout(function () {
        alert.style.transition = "opacity .4s ease";
        alert.style.opacity = "0";
        window.setTimeout(function () { alert.remove(); }, 450);
      }, 5200);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    animateBars();
    autoDismissAlerts();
  });

  window.CQ = { post: post, toast: toast, readJson: readJson };
})();
