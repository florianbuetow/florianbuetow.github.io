# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-05-24

### Added

- Added Wardley map rendering pipeline via `wtg2svg` with blog-themed styled SVG output.
- Added `check-code-line-length` build check flagging draft code block lines over 76 characters.

### Changed

- Improved project pages with richer images and higher-fidelity preview thumbnails.
- Updated home page bio and newsletter call-to-action copy.
- Renamed ticker article titles to consistent "Claude Plugin/Code" naming format.
- Improved Pagefind index build reliability with mandatory rebuild and added validation step.

### Fixed

- Fixed sidebar date visibility for pages without a date set.

## 2026-05-20

### Added

- Added site-wide full-text search powered by Pagefind, rebuilt on each deploy.
- Added combined RSS feed at `/feed.xml` aggregating blog and ticker posts.

### Changed

- Redesigned Resources page as a linked table pointing to GitHub repositories.
- Updated project listing and individual detail pages across the site.
- Logo updated to WebP; table of contents now includes the page title.

### Fixed

- Fixed deprecated locale field in RSS feed output.

## 2026-05-16

### Added

- Launched new Hugo-based site, replacing the previous MkDocs setup.
- Added Mermaid diagram rendering and zoomable image lightbox for articles.
- Added image optimization pipeline converting all images to WebP automatically.
- Added Resources page with links to open-source projects and tools.

### Changed

- Sidenotes now float into the right article column.
- Dev server now shows drafts, future-dated, and expired posts.

### Fixed

- Fixed navigation menu wrapping in Firefox.
- Removed debug toggle button from the live site.

## 2025-02-23

### Added

- Added user manual section.

### Changed

- Updated user manual content.

## 2025-01-13

### Added

- Initial site with blog articles and RSS feed.

### Changed

- Updated CNAME for custom domain routing.
