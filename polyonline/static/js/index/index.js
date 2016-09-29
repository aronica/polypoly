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
    ,
    width:$(document).width(),
    height:$(document).width()*0.4
  })


  $('#layout-slides-left').slidesjs({
    navigation: {
      active: false
    },
    pagination: {
      active: true,
      effect: 'slide'
    },
    width:$(document).width(),
    height:$(document).width()
  })

  var width1 = 633;
  var height1 = 253;

if(isMobile=="true") {
  width1 = $(document).width();
  height1 = width1 * 0.38;
}
  $('#layout-slides').slidesjs({
    navigation: {
        active: false
    },
    pagination: {
        active: true,
        effect: 'slide'
    },
    width: width1,
    height: height1
  })
})()
