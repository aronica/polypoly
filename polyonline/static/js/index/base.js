new Vue({
  el: '#header-title',
  showNav: false,
  methods: {
    toggle: function() {
      var nav = document.querySelector('.header-nav')
      if (nav.style.display !== 'none') {
        nav.style.display = 'none'
      } else {
        nav.style.display = 'block'
      }   
    }
  }
})

