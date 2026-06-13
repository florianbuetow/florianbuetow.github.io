/*
 * In-place filtering for the article and ticker list pages.
 *
 * The entire section is rendered into the page, so filtering is GLOBAL: clicking
 * a category or tag pill shows every matching post regardless of which
 * pagination page it would otherwise fall on. When .post-list carries a
 * data-page-size attribute the matching set is paginated client-side (resetting
 * to page 1 on every filter change); without it, all matches are shown.
 *
 * Pills carry data-kind ("category"|"tag") and data-term (display name); each
 * .post carries comma-separated data-categories / data-tags. Matching is
 * case-insensitive (Hugo humanises term names but never alters their structure),
 * with OR within a group and AND across the two groups.
 */
(function () {
  var sidebar = document.querySelector(".filter-sidebar");
  var postList = document.querySelector(".post-list");
  if (!sidebar || !postList) return;

  var pills = toArray(sidebar.querySelectorAll(".pill"));
  var posts = toArray(postList.querySelectorAll(".post"));
  if (!pills.length || !posts.length) return;

  var clearBtn = sidebar.querySelector(".filter-clear");
  var nav = postList.querySelector("[data-pagination]");
  var navDivider = postList.querySelector("[data-pagination-divider]");
  var pageSize = parseInt(postList.getAttribute("data-page-size"), 10);
  if (!(pageSize > 0)) pageSize = 0; // 0 => no pagination, show every match

  var currentPage = 1;
  var emptyEl = null;

  for (var i = 0; i < posts.length; i++) {
    posts[i]._cats = splitTerms(posts[i].getAttribute("data-categories"));
    posts[i]._tags = splitTerms(posts[i].getAttribute("data-tags"));
  }

  bindClick(pills, function (pill) {
    pill.classList.toggle("active");
    currentPage = 1;
    render();
  });

  if (clearBtn) {
    clearBtn.addEventListener("click", function (e) {
      e.preventDefault();
      for (var j = 0; j < pills.length; j++) pills[j].classList.remove("active");
      currentPage = 1;
      render();
    });
  }

  render();

  function render() {
    var cats = activeTerms("category");
    var tags = activeTerms("tag");
    var hasFilter = cats.length > 0 || tags.length > 0;

    var matching = [];
    for (var k = 0; k < posts.length; k++) {
      if (matchesPost(posts[k], cats, tags)) matching.push(posts[k]);
    }

    var totalPages = pageSize ? Math.max(1, Math.ceil(matching.length / pageSize)) : 1;
    if (currentPage > totalPages) currentPage = totalPages;

    var start = pageSize ? (currentPage - 1) * pageSize : 0;
    var end = pageSize ? start + pageSize : matching.length;

    for (var m = 0; m < posts.length; m++) posts[m]._show = false;
    for (var n = start; n < end && n < matching.length; n++) matching[n]._show = true;
    for (var p = 0; p < posts.length; p++) {
      posts[p].classList.toggle("hidden", !posts[p]._show);
    }

    updateDividers();
    updateEmpty(matching.length === 0);
    updateNav(totalPages);
    if (clearBtn) clearBtn.classList.toggle("visible", hasFilter);
  }

  function activeTerms(kind) {
    var out = [];
    for (var i = 0; i < pills.length; i++) {
      if (pills[i].classList.contains("active") && pills[i].getAttribute("data-kind") === kind) {
        out.push(norm(pills[i].getAttribute("data-term")));
      }
    }
    return out;
  }

  function matchesPost(post, cats, tags) {
    var catOk = cats.length === 0 || hasAny(post._cats, cats);
    var tagOk = tags.length === 0 || hasAny(post._tags, tags);
    return catOk && tagOk;
  }

  // A divider between two posts is shown only when a visible post precedes it
  // and the post immediately after it is also visible. The pagination divider
  // is left to updateNav().
  function updateDividers() {
    var seenVisible = false;
    var children = toArray(postList.children);
    for (var i = 0; i < children.length; i++) {
      var el = children[i];
      if (el.classList.contains("post")) {
        if (!el.classList.contains("hidden")) seenVisible = true;
      } else if (el.classList.contains("divider") && !el.hasAttribute("data-pagination-divider")) {
        var next = el.nextElementSibling;
        if (next && next.classList.contains("post")) {
          el.classList.toggle("hidden", !(seenVisible && !next.classList.contains("hidden")));
        }
      }
    }
  }

  function updateEmpty(show) {
    if (show && !emptyEl) {
      emptyEl = document.createElement("p");
      emptyEl.className = "filter-empty";
      emptyEl.textContent = "No posts match the selected filters.";
      postList.insertBefore(emptyEl, postList.firstChild);
    }
    if (emptyEl) emptyEl.classList.toggle("hidden", !show);
  }

  function updateNav(totalPages) {
    var show = pageSize > 0 && totalPages > 1;
    if (navDivider) navDivider.classList.toggle("hidden", !show);
    if (!nav) return;
    nav.classList.toggle("hidden", !show);
    nav.innerHTML = "";
    if (!show) return;
    nav.appendChild(navLink("← Newer", currentPage > 1, -1));
    var info = document.createElement("span");
    info.className = "pagination-info";
    info.textContent = "Page " + currentPage + " of " + totalPages;
    nav.appendChild(info);
    nav.appendChild(navLink("Older →", currentPage < totalPages, 1));
  }

  function navLink(label, enabled, delta) {
    var a = document.createElement("a");
    a.className = "pagination-link" + (enabled ? "" : " pagination-disabled");
    a.href = "#";
    a.textContent = label;
    a.addEventListener("click", function (e) {
      e.preventDefault();
      if (!enabled) return;
      currentPage += delta;
      render();
      if (postList.scrollIntoView) postList.scrollIntoView({ block: "start" });
    });
    return a;
  }

  function bindClick(els, fn) {
    for (var i = 0; i < els.length; i++) {
      (function (el) {
        el.addEventListener("click", function (e) {
          e.preventDefault();
          fn(el);
        });
      })(els[i]);
    }
  }

  function hasAny(haystack, needles) {
    for (var i = 0; i < needles.length; i++) {
      if (haystack.indexOf(needles[i]) !== -1) return true;
    }
    return false;
  }
  function splitTerms(raw) {
    var parts = (raw || "").split(",");
    var out = [];
    for (var i = 0; i < parts.length; i++) {
      var v = norm(parts[i]);
      if (v) out.push(v);
    }
    return out;
  }
  function norm(s) { return (s || "").trim().toLowerCase(); }
  function toArray(nl) { return Array.prototype.slice.call(nl); }
})();
