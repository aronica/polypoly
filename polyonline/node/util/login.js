'use strict'
/**
 * @author: puju
 * @createdTime: 2016-08-26 17:37:41
 * @fileName: login.js
 * @description:
 **/
const request = require('./request')
const config = require('../config/config')
const co = require('co')

const checkLogin = co.wrap(function *(openid) {
    let data = {
      uri: config.host + '/user/weixin/get',
      method: 'GET',
      json: true,
      qs: {
        openid: openid
      }
    }

    return request(data)
})

module.exports = {
  checkLogin: checkLogin
}
