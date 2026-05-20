(function () {
    var toc = document.querySelector('#TableOfContents');
    var h1 = document.querySelector('.article-body h1');
    if (h1 && h1.id && toc) {
        var ul = toc.querySelector('ul');
        if (ul) {
            var li = document.createElement('li');
            var a = document.createElement('a');
            a.href = '#' + h1.id;
            a.textContent = h1.textContent;
            li.appendChild(a);
            ul.insertBefore(li, ul.firstChild);
        }
    }

    var headings = document.querySelectorAll('.article-body h1, .article-body h2, .article-body h3');
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
