module.exports = {
  release: {
    files: [{
      cwd: '<%= source_dir %>/src',
      src: '**/*.tpl.html',
      dest: '<%= temp_dir %>/js/app.templates.js'
    }],
    options: {
      module: 'myApp',
      htmlmin: {
        collapseBooleanAttributes:      true,
        collapseWhitespace:             true,
        removeAttributeQuotes:          true,
        removeComments:                 true, // Only if you don't use comment directives!
        removeEmptyAttributes:          true,
        removeRedundantAttributes:      true,
        removeScriptTypeAttributes:     true,
        removeStyleLinkTypeAttributes:  true
      }
    }
  }
}
