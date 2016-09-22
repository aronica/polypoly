  if(document.querySelector('.login-right')){
    document.querySelector('.login-right').onclick = function() {
      window.location.href = 'personal.html'
    }
  }

  //document.addEventListener('click', function() {
  //  var el = document.querySelector('#select-container .select-options')
  //  if (el) {
  //    document.querySelector('#select-container .select-options').style.display = 'none'
  //  }
  //})

  new Vue({
    el: '#select-container',
    data: {
      selected: ''
    },
    methods: {
      toggleOptions: function(item) {
        console.log(item)
        var el = document.querySelector('#select-container .select-options')
        if (el.style.display === 'none' || el.style.display === '') {
          el.style.display = 'block'
        } else {
          el.style.display = 'none'
        }

      },
      selectOptions: function(item) {
        console.log(item)
        document.querySelector('#select-container .select-options').style.display = 'none'
        var url = location.href.replace(location.search, '')
        if(item === '全部城市'){
          window.location.href = url;
          return;
        }
        window.location.href = url + '?city=' + item
      }
    }
  })
