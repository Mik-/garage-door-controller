module.exports = {
  gruntfile: {
    files: ['Gruntfile.js', 'grunt/**'],
    options: {
      reload: true
    }
  },
  sass: {
    files: '<%= source_dir %>/scss/**/*.scss',
    tasks: ['sass:release', 'autoprefixer:release', 'concat:fontawesome', 'cssmin:release'],
    options: {
      spawn: false
    }
  },
  js: {
    files: ['<%= source_dir %>/src/**/*.js', '<%= source_dir %>/src/**/*.tpl.html'],
    tasks: ['ngtemplates:release', 'concat:release'],
    options: {
      spawn: false
    }
  },
  html: {
    files: ['<%= source_dir %>/html/**/*.html'],
    tasks: ['copy:release'],
    options: {
      spawn: false
    }
  }
}
