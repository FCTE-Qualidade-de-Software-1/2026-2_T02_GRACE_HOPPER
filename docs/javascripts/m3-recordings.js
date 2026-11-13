/* Amplia as gravações da M3; os links abrem o GIF quando JavaScript não está disponível. */
(function () {
  "use strict";

  function initializeRecordings() {
    var dialog = document.getElementById("m3-recording-dialog");
    if (!dialog || typeof dialog.showModal !== "function" || dialog.dataset.initialized) return;
    dialog.dataset.initialized = "true";

    var title = dialog.querySelector("#m3-recording-title");
    var caption = dialog.querySelector("#m3-recording-caption");
    var media = dialog.querySelector(".m3-recording-dialog-media");
    var original = dialog.querySelector(".m3-recording-original");
    var trigger = null;

    document.querySelectorAll(".m3-recording-card").forEach(function (card) {
      card.addEventListener("click", function (event) {
        if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        trigger = card;
        title.textContent = card.dataset.recordingTitle;
        caption.textContent = card.dataset.recordingCaption;
        original.href = card.href;

        var image = document.createElement("img");
        image.src = card.href;
        image.alt = card.querySelector("img").alt;
        image.width = 1609;
        image.height = 814;
        media.replaceChildren(image);
        dialog.showModal();
        document.documentElement.classList.add("m3-recording-open");
      });
    });

    dialog.querySelector(".m3-recording-close").addEventListener("click", function () {
      dialog.close();
    });

    dialog.addEventListener("click", function (event) {
      if (event.target !== dialog) return;
      var bounds = dialog.getBoundingClientRect();
      if (event.clientX < bounds.left || event.clientX > bounds.right ||
          event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
    });

    dialog.addEventListener("close", function () {
      document.documentElement.classList.remove("m3-recording-open");
      media.replaceChildren();
      if (trigger && trigger.isConnected) trigger.focus({ preventScroll: true });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeRecordings);
  } else {
    initializeRecordings();
  }
})();
