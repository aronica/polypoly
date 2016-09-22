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

  $('#layout-slides-left').slidesjs({
    navigation: {
      active: false
    },
    pagination: {
      active: true,
      effect: 'slide'
    },
    width:337,
    height:303
  })

  $('#layout-slides').slidesjs({
    navigation: {
        active: false
    },
    pagination: {
        active: true,
        effect: 'slide'
    },
    width: '633',
    height: '293'
  })
})()
