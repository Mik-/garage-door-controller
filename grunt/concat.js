module.exports = {
  release: {
    options: {},
    files: [{
      src: [
        '<%= source_dir %>/src/**/module.js',
        '<%= source_dir %>/src/app.js',
        '<%= temp_dir %>/js/app.templates.js',
        '<%= source_dir %>/src/**/*.js',
        '!<%= source_dir %>/src/**/*_test.js'
      ],
      dest: '<%= release_dir %>/js/app.js'
    }, {
      src: [
        '<%= bower_dir %>/angular/angular.js',
        '<%= bower_dir %>/angular-route/angular-route.js'
      ],
      dest: '<%= release_dir %>/js/libs.js'
    }]
  }
}
