module.exports = {
  release: {
    files: [
      {
        expand: true,
        cwd: '<%= source_dir %>/html',
        src: ['**/*.html'],
        dest: '<%= release_dir %>/'
      },
      {
        src: '<%= bower_dir %>/html5-boilerplate/dist/js/vendor/modernizr-2.8.3.min.js',
        dest: '<%= release_dir %>/js/modernizr.js'
      }
    ]
  }
}
