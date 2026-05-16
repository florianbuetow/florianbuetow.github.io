(function () {
  var dialog = document.createElement("dialog");
  dialog.className = "lightbox-dialog";
  var img = document.createElement("img");
  dialog.appendChild(img);
  document.body.appendChild(dialog);

  dialog.addEventListener("click", function () {
    dialog.close();
  });

  function open(src, alt, natW, natH) {
    img.src = src;
    img.alt = alt;
    var vw = window.innerWidth - 48;
    var vh = window.innerHeight - 48;
    var scale = Math.min(1, vw / natW, vh / natH);
    img.style.width = Math.round(natW * scale) + "px";
    img.style.height = Math.round(natH * scale) + "px";
    dialog.showModal();
  }

  document.querySelectorAll(".article-body img.zoomable").forEach(function (el) {
    el.addEventListener("click", function () {
      var src = el.getAttribute("data-zoom-src") || el.src;
      var natW = el.naturalWidth;
      var natH = el.naturalHeight;
      var hdImg = new Image();
      hdImg.onload = function () {
        open(src, el.alt, hdImg.naturalWidth, hdImg.naturalHeight);
      };
      hdImg.src = src;
      if (hdImg.complete) {
        open(src, el.alt, hdImg.naturalWidth, hdImg.naturalHeight);
      }
    });
  });
})();
