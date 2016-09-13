var EXPORT = new Vue({
  el: '#content',
  data: {
    name: '125Y-a(B)',
    visibility: 'hidden',
    city: '佛山',
    house: '',
    item: 'structure',
    cities: ['佛山', '江门'],
    names: [
      '125Y-a(B)',
      '125Y-b(N)',
      '140Y-a(N)',
      '140Y-b(B)',
      '140Y-c(N)',
      '140Y-d(N)',
      '140Y-e(N)',
      '90W-a(N)',
      '90W-b(N)'
    ]
  },
  methods: {
    changeOption: function(item) {
      this.item = item
      var els = document.querySelectorAll('.bar-list')
      for (var index = 0, l = els.length; index < l; ++index) {
        els[index].style.backgroundColor = '#444'
      }
      var target = this.$event.currentTarget
      target.style.backgroundColor = '#1e46a1'

      var el = document.querySelector('.houses')
      if (item === 'comment') {
          el.style.visibility = 'visible'
      } else {
          el.style.visibility = 'hidden'
      }
    }
  }
})

