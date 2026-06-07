(function () {
  var config = window.__draftAnnotator;
  if (!config || !config.enabled || !config.filePath) return;
  if (window.location.hostname !== "127.0.0.1" && window.location.hostname !== "localhost") return;

  var article = document.querySelector(".article-body");
  if (!article) return;

  var endpoint = config.endpoint || "http://127.0.0.1:8787/draft-annotation";
  var blockSelector = "p, li, blockquote, h2, h3, h4, .side-note, .side-quote";
  var ignoredSelector = "a, button, input, textarea, select, pre, code, dialog";
  var dialog = null;
  var quoteInput = null;
  var noteInput = null;
  var statusEl = null;
  var lastBlock = null;

  function createDialog() {
    dialog = document.createElement("dialog");
    dialog.className = "draft-annotation-dialog";

    var form = document.createElement("form");
    form.method = "dialog";
    form.className = "draft-annotation-form";

    var title = document.createElement("h2");
    title.textContent = "Draft annotation";

    var quoteLabel = document.createElement("label");
    quoteLabel.textContent = "Quote";
    quoteInput = document.createElement("textarea");
    quoteInput.name = "quote";
    quoteInput.rows = 4;
    quoteInput.required = true;
    quoteLabel.appendChild(quoteInput);

    var noteLabel = document.createElement("label");
    noteLabel.textContent = "Annotation";
    noteInput = document.createElement("textarea");
    noteInput.name = "note";
    noteInput.rows = 5;
    noteInput.required = true;
    noteLabel.appendChild(noteInput);

    statusEl = document.createElement("p");
    statusEl.className = "draft-annotation-status";
    statusEl.setAttribute("role", "status");

    var actions = document.createElement("div");
    actions.className = "draft-annotation-actions";

    var cancel = document.createElement("button");
    cancel.type = "button";
    cancel.textContent = "Cancel";
    cancel.addEventListener("click", closeDialog);

    var save = document.createElement("button");
    save.type = "submit";
    save.textContent = "Save annotation";

    actions.appendChild(cancel);
    actions.appendChild(save);
    form.appendChild(title);
    form.appendChild(quoteLabel);
    form.appendChild(noteLabel);
    form.appendChild(statusEl);
    form.appendChild(actions);
    dialog.appendChild(form);
    document.body.appendChild(dialog);

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      saveAnnotation(save);
    });
  }

  function normalizeText(text) {
    return text.replace(/\s+/g, " ").trim();
  }

  function readableBlockText(block) {
    var clone = block.cloneNode(true);
    if (clone.classList && clone.classList.contains("side-note")) {
      clone.querySelectorAll("strong").forEach(function (el) {
        el.remove();
      });
    }
    if (clone.classList && clone.classList.contains("side-quote")) {
      clone.querySelectorAll("cite").forEach(function (el) {
        el.remove();
      });
    }
    return normalizeText(clone.textContent || "");
  }

  function quoteForBlock(block) {
    var selected = normalizeText(String(window.getSelection()));
    var blockText = readableBlockText(block);
    if (selected.length >= 16 && blockText.indexOf(selected) !== -1) {
      return selected;
    }
    return blockText.slice(0, 600);
  }

  function openDialog(block) {
    if (!dialog) createDialog();
    lastBlock = block;
    quoteInput.value = quoteForBlock(block);
    noteInput.value = "";
    statusEl.textContent = "";
    dialog.showModal();
    window.setTimeout(function () {
      noteInput.focus();
    }, 0);
  }

  function closeDialog() {
    if (dialog && dialog.open) dialog.close();
    lastBlock = null;
  }

  function setStatus(message, isError) {
    statusEl.textContent = message;
    statusEl.dataset.state = isError ? "error" : "ok";
  }

  function saveAnnotation(button) {
    var quote = quoteInput.value.trim();
    var note = noteInput.value.trim();
    if (!quote || !note) {
      setStatus("Quote and annotation are required.", true);
      return;
    }
    button.disabled = true;
    setStatus("Saving...", false);

    fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        filePath: config.filePath,
        relPermalink: config.relPermalink || window.location.pathname,
        quote: quote,
        note: note
      })
    })
      .then(function (response) {
        return response.json().then(function (payload) {
          if (!response.ok || !payload.ok) {
            throw new Error(payload.error || "Could not save annotation.");
          }
          return payload;
        });
      })
      .then(function () {
        if (lastBlock) lastBlock.classList.add("draft-annotation-saved");
        setStatus("Saved.", false);
        window.setTimeout(closeDialog, 250);
      })
      .catch(function (error) {
        var message = error && error.message ? error.message : "";
        if (/failed|load|network/i.test(message)) {
          message = "Could not reach the draft annotator. Run `just draft-annotator` in another terminal.";
        }
        setStatus(message || "Could not save annotation.", true);
      })
      .finally(function () {
        button.disabled = false;
      });
  }

  article.addEventListener("dblclick", function (event) {
    if (event.target.closest(ignoredSelector)) return;
    var block = event.target.closest(blockSelector);
    if (!block || !article.contains(block)) return;
    openDialog(block);
  });
})();
