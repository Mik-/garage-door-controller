module.exports = {
  release: {
    expand: true,
    cwd: '<%= temp_dir %>/css',
    src: ['*.css'],
    dest: '<%= release_dir %>/css'
  }
}
