module.exports = {
  release: {
    options: {
      cacheLocation: '<%= temp_dir %>/.sass-cache',
      update: true
    },
    files: [{
      expand: true,
      cwd: '<%= source_dir %>/scss',
      src: ['**/*.scss', '!**/_*.scss'],
      dest: '<%= temp_dir %>/css',
      ext: '.css'
    }]
  }
}
