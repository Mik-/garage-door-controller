module.exports = {
  release: {
    expand: true,
    cwd: '<%= temp_dir %>/css',
    src: ['**/*.css'],
    dest: '<%= temp_dir %>/css',
  }
}
