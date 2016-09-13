function getQueryString() {
  var qs = location.search.replace('?', '').split('&')
  var data = {}
  for (var i = 0, l = qs.length; i < l; ++i) {
    var item = qs[i].split('=')
    data[item[0]] = item[1]
  }
  return data
}

new Vue({
  el: '#select-container-1',
  data: {
    areaModel: '-',
    structureModel: '-'
  },
  methods: {
    toggleOptions: function(item) {
      var el = document.querySelector('#select-container-1 .select-options')
      console.log(el.style.display)
      if (el.style.display === 'none' || el.style.display === '') {
        el.style.display = 'block'
      } else {
        el.style.display = 'none'
      }
    },
    selectOptions: function(item, e) {
      console.log(item)
      var area_value = e.target.getAttribute('value')
      var structure_value = document.querySelector('#select-container-2 .selected').getAttribute('value')
      var property_id = getQueryString().property_id || ''
      var url = location.href.replace(location.search, '')
      window.location.href = url + '?property_id=' + property_id + '&area_value=' + area_value + '&structure_value=' + structure_value
    }
  }
})

new Vue({
  el: '#select-container-2',
  data: {
    areaModel: '-',
    structureModel: '-'
  },
  methods: {
    toggleOptions: function(item) {
      console.log(item)
      var el = document.querySelector('#select-container-2 .select-options')
      if (el.style.display === 'none' || el.style.display === '') {
        el.style.display = 'block'
      } else {
        el.style.display = 'none'
      }
    },
    selectOptions: function(item, e) {
      console.log(item, e.target)
      var area_value = document.querySelector('#select-container-1 .selected').getAttribute('value')
      var structure_value = e.target.getAttribute('value')
      var property_id = getQueryString().property_id || ''
      var url = location.href.replace(location.search, '')
      window.location.href = url + '?property_id=' + property_id + '&area_value=' + area_value + '&structure_value=' + structure_value
    }
  }
})
