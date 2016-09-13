'use strict'
/**
 * @author: puju
 * @createdTime: 2016-08-24 17:45:32
 * @fileName: ../../js/index/test.js
 * @description:
 **/

;(function() {
  window.LOGIN = new Vue({
    el: '#login',
    data: {
      text: '点击登录'
    },
    methods: {
      login: function() {
        if (window.confirm('登录')) {
          window.location.href='/login.html'
        }
      }
    }
  })
})()
