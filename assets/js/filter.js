(function () {
    var posts = document.querySelectorAll('.post');
    if (!posts.length) return;

    var dividers = document.querySelectorAll('.divider');
    var search = document.getElementById('search-input');
    var sidebar = document.getElementById('filter-sidebar');
    var noResults = document.getElementById('no-results');
    if (!sidebar || !search) return;

    var activeCats = new Set();
    var activeTags = new Set();
    var allCats = new Set();
    var allTags = new Set();

    posts.forEach(function (p) {
        (p.dataset.categories || '').split(',').forEach(function (c) { if (c) allCats.add(c.trim()); });
        (p.dataset.tags || '').split(',').forEach(function (t) { if (t) allTags.add(t.trim()); });
    });

    function buildSidebar() {
        var html = '';
        if (allCats.size > 0) {
            html += '<div class="filter-section"><h4>Categories</h4><div class="filter-pills">';
            Array.from(allCats).sort().forEach(function (c) {
                html += '<button class="pill" data-type="category" data-value="' + c + '">' + c + '</button>';
            });
            html += '</div></div>';
        }
        if (allTags.size > 0) {
            html += '<div class="filter-section"><h4>Tags</h4><div class="filter-pills">';
            Array.from(allTags).sort().forEach(function (t) {
                html += '<button class="pill" data-type="tag" data-value="' + t + '">' + t + '</button>';
            });
            html += '</div></div>';
        }
        html += '<button class="filter-clear" id="filter-clear">Clear all filters</button>';
        sidebar.innerHTML = html;

        sidebar.querySelectorAll('.pill').forEach(function (pill) {
            pill.addEventListener('click', function () {
                var set = pill.dataset.type === 'category' ? activeCats : activeTags;
                var val = pill.dataset.value;
                if (set.has(val)) { set.delete(val); } else { set.add(val); }
                pill.classList.toggle('active');
                filter();
            });
        });
        var clearBtn = document.getElementById('filter-clear');
        if (clearBtn) clearBtn.addEventListener('click', clear);
    }

    function clear() {
        activeCats.clear();
        activeTags.clear();
        search.value = '';
        sidebar.querySelectorAll('.pill').forEach(function (p) { p.classList.remove('active'); });
        filter();
    }

    function filter() {
        var q = search.value.toLowerCase().trim();
        var hasFilters = activeCats.size > 0 || activeTags.size > 0 || q.length > 0;
        var visible = 0;

        posts.forEach(function (post) {
            var cats = (post.dataset.categories || '').split(',').map(function (s) { return s.trim(); });
            var tags = (post.dataset.tags || '').split(',').map(function (s) { return s.trim(); });
            var text = post.textContent.toLowerCase();
            var ok = (activeCats.size === 0 || cats.some(function (c) { return activeCats.has(c); }))
                  && (activeTags.size === 0 || tags.some(function (t) { return activeTags.has(t); }))
                  && (q.length === 0 || text.includes(q));
            post.classList.toggle('hidden', !ok);
            if (ok) visible++;
        });

        dividers.forEach(function (d) { d.classList.add('hidden'); });
        var shown = Array.from(posts).filter(function (p) { return !p.classList.contains('hidden'); });
        shown.forEach(function (p, i) {
            if (i < shown.length - 1) {
                var el = p.nextElementSibling;
                while (el && !el.classList.contains('divider')) el = el.nextElementSibling;
                if (el) el.classList.remove('hidden');
            }
        });

        if (noResults) noResults.classList.toggle('visible', visible === 0);
        var clearBtn = document.getElementById('filter-clear');
        if (clearBtn) clearBtn.classList.toggle('visible', hasFilters);
    }

    buildSidebar();
    search.addEventListener('input', filter);
    search.addEventListener('keydown', function (e) { e.stopPropagation(); });
})();
