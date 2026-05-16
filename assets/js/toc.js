(function () {
    var headings = document.querySelectorAll('.article-body h2, .article-body h3');
    var tocLinks = document.querySelectorAll('#TableOfContents a, .toc-item a');
    if (!headings.length || !tocLinks.length) return;

    function update() {
        var scrollY = window.scrollY + 100;
        var current = '';
        headings.forEach(function (h) {
            if (h.offsetTop <= scrollY) current = h.id;
        });
        tocLinks.forEach(function (a) {
            a.classList.toggle('active', a.getAttribute('href') === '#' + current);
        });
    }
    window.addEventListener('scroll', update, { passive: true });
    update();
})();
