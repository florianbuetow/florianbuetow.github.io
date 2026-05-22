(function () {
    var input = document.getElementById('search-input');
    if (!input) return;

    var searchBox = input.closest('.search-box');
    if (!searchBox) return;

    var resultsEl = document.createElement('div');
    resultsEl.id = 'search-results';
    resultsEl.hidden = true;
    searchBox.appendChild(resultsEl);

    var pagefind = null;
    var pagefindLoad = null;

    function loadPagefind() {
        if (pagefind) return Promise.resolve(pagefind);
        if (pagefindLoad) return pagefindLoad;
        pagefindLoad = import('/pagefind/pagefind.js')
            .then(function (mod) {
                pagefind = mod;
                return pagefind;
            })
            .catch(function (err) {
                if (typeof console !== 'undefined' && console.warn) {
                    console.warn('[global-search] failed to load /pagefind/pagefind.js; search disabled. Run `just build-pagefind-index` (or `just build`) to rebuild the index.', err);
                }
                pagefind = null;
                pagefindLoad = null;
                return null;
            });
        return pagefindLoad;
    }

    function hideResults() {
        resultsEl.hidden = true;
        resultsEl.innerHTML = '';
    }

    function getSnippet(data) {
        if (data.excerpt) return data.excerpt;
        if (data.content) return data.content.slice(0, 180);
        return '';
    }

    async function renderResults(query) {
        var pf = await loadPagefind();
        if (!pf || typeof pf.search !== 'function') {
            hideResults();
            return;
        }

        try {
            var response = await pf.search(query);
            var matches = response && response.results ? response.results.slice(0, 8) : [];
            if (matches.length === 0) {
                hideResults();
                return;
            }

            var html = [];
            for (var i = 0; i < matches.length; i++) {
                var data = await matches[i].data();
                html.push(
                    '<a class="search-result-item" href="' + data.url + '">' +
                    '<strong>' + data.meta.title + '</strong>' +
                    '<p>' + getSnippet(data) + '</p>' +
                    '<span>' + data.url + '</span>' +
                    '</a>'
                );
            }
            resultsEl.innerHTML = html.join('');
            resultsEl.hidden = false;
        } catch (error) {
            hideResults();
        }
    }

    input.addEventListener('input', function () {
        var query = input.value.trim();
        if (!query) {
            hideResults();
            return;
        }
        renderResults(query);
    });

    input.addEventListener('focus', function () {
        var query = input.value.trim();
        if (query) renderResults(query);
    });

    input.addEventListener('blur', function () {
        window.setTimeout(hideResults, 120);
    });

    input.addEventListener('keydown', function (event) {
        if (event.key !== 'Enter') return;
        var first = resultsEl.querySelector('.search-result-item');
        if (!first || resultsEl.hidden) return;
        event.preventDefault();
        window.location.href = first.href;
    });
})();
