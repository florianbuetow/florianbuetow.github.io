module.exports = {
  ci: {
    collect: {
      staticDistDir: './public',
      url: [
        'http://localhost/',
        'http://localhost/blog/',
        'http://localhost/ticker/',
        'http://localhost/projects/',
        'http://localhost/resources/',
      ],
      numberOfRuns: 3,
    },
    assert: {
      preset: 'lighthouse:recommended',
      assertions: {
        'categories:performance': ['error', { minScore: 0.7 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
        'categories:best-practices': ['error', { minScore: 0.9 }],
        'categories:seo': ['error', { minScore: 0.9 }],
        // Baseline existing site issues as warnings so CI can adopt LHCI first.
        'color-contrast': ['warn', { minScore: 0.9 }],
        'errors-in-console': ['warn', { minScore: 0.9 }],
        'image-delivery-insight': ['warn', { minScore: 0.9 }],
        'lcp-discovery-insight': ['warn', { minScore: 0.9 }],
        'meta-description': ['warn', { minScore: 0.9 }],
        'network-dependency-tree-insight': ['warn', { minScore: 0.9 }],
        'target-size': ['warn', { minScore: 0.9 }],
        'unsized-images': ['warn', { minScore: 0.9 }],
        'uses-responsive-images': ['warn', { maxLength: 0 }],
      },
    },
    upload: {
      target: 'filesystem',
      outputDir: './reports/lighthouse',
      reportFilenamePattern: '%%PATHNAME%%-%%DATETIME%%.report.%%EXTENSION%%',
    },
  },
};
