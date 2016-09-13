'use strict'
/**
 * @author: ke.wu
 * @create_time: 2016-07-28 11:13:57
 * @file_name: index.js
 * @description:
 **/
;(function() {
  $('#banner-slides').slidesjs({
    navigation: {
      active: false
    },
    pageination: {
      active: true,
      effect: 'slide'
    }
  })
  $('#layout-slides').slidesjs({
    navigation: {
        active: false
    },
    pagination: {
        active: true,
        effect: 'slide'
    }
  })
})()
