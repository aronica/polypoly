'use strict'
/**
 * @author: Ke Wu
 * @createdTime: 2016-08-09 14:32:47
 * @fileName: js/index/comment.js
 * @description:
 **/


function getQuerystring() {
  var qs = window.location.search.replace('?', '').split('&')
  var ret = {}
  for (var index = 0, l = qs.length; index < l; ++index) {
    var item = qs[index].split('=')
    ret[item[0]] = item[1]
  }
  return ret
}

function submitData() {
  var qs = getQuerystring()
  var url = '/comment?structure_id=' + (qs.structure_id || '') + '&property_id=' + (qs.property_id || '')
  $.ajax({
    url: url,
    type: 'POST',
    data: {
      comment: {
        hall_comment: COMMENTS.hall_comment,
        hall_score: COMMENTS.hall_score,
        kitchen_comment: COMMENTS.dinning_hall_comment,
        kitchen_score: COMMENTS.dining_score,
        bedroom_comment: COMMENTS.bedroom_comment,
        bedroom_score: COMMENTS.bedroom_score,
        toilet_comment: COMMENTS.toilet_comment,
        toilet_score: COMMENTS.toilet_score,
        overview_comment: COMMENTS.overview_comment,
        overview_score: COMMENTS.overview_score
      },
      title: ALERT.title,
      phone: ALERT.phone,
      estimatedTime: ALERT.estimated_time
    },
    dataType: 'json',
    success: function(res, xhr, e) {
      console.log(res, xhr, e)
      SHARE.el.style.display = 'block';
      // alert('您已成功提价评价，谢谢您的反馈！')
    },
    error: function(res, xhr, e) {

    }
  })
}

if (isMobile) {
    $('.sketchfab-embed-wrapper').html('<iframe width="100%" height="300px" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" onmousewheel="" name="sketchfabModel" src=https://sketchfab.com/models/' + MODELS + '/embed?autostart=1&preload=1&ui_controls=0&ui_infos=0">')
} else {
    $('.sketchfab-embed-wrapper').html('<iframe width="100%" height="592px" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" onmousewheel="" name="sketchfabModel" src=https://sketchfab.com/models/' + MODELS + '/embed?autostart=1&preload=1&ui_controls=0&ui_infos=0">')
}


var NEW_STAR = ''
var OLD_STAR = '㒅'
var ALERT = new Vue({
  el: '#addtional-info',
  data: {
    title: '',
    phone: '',
    estimated_time: '3个月内',
    showAddtionalInfo: false,
    el: document.querySelector('.addtional-info')
  },
  methods: {
    cancel: function() {
      this.el.style.display = 'none'
      // submitData()
    },
    'confirm': function() {
      this.el.style.display = 'none'
      submitData()
    }
  }
})

var SHARE = new Vue({
  el: '#share-info',
  data: {
    title: '',
    phone: '',
    estimated_time: '',
    showShareInfo: false,
    el: document.querySelector('.share-info')
  },
  methods: {
    cancel: function() {
      this.el.style.display = 'none'
      // submitData()
    },
    'confirm': function() {
      this.el.style.display = 'none'
      // submitData()
    }
  }
})

var COMMENTS = new Vue({
  el: '#comments',
  data: {
    hall_comment: '',
    dinning_hall_comment: '',
    bedroom_comment: '',
    toilet_comment: '',
    overview_comment: '',
    hall_stars: ['㒅', '㒅', '㒅', '㒅', '㒅'],
    hall_score: 0,
    bedroom_stars: ['㒅', '㒅', '㒅', '㒅', '㒅'],
    bedroom_score: 0,
    toilet_stars: ['㒅', '㒅', '㒅', '㒅', '㒅'],
    toilet_score: 0,
    dining_stars: ['㒅', '㒅', '㒅', '㒅', '㒅'],
    dining_score: 0,
    overview_stars: ['㒅', '㒅', '㒅', '㒅', '㒅'],
    overview_score: 0
  },
  methods: {
    scoreMouseOver: function(index, d) {
      for (var i = 0; i <= index; ++i) {
         this[d + '_stars'].$set(i, NEW_STAR)
      }

      for (var i = 4; i > index; i--) {
        this[d + '_stars'].$set(i, OLD_STAR)
      }

      this[d + '_score'] = index + 1
    },
    submit: function() {
      ALERT.el.style.display = 'block'
    }
  }
})

