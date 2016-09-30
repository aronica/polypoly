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

const getAccessToken = co.wrap(function *(){
    let data = {
        url: "https://api.weixin.qq.com/cgi-bin/token",
        method: "get",
        json: true,
        qs: {
            grant_type: "client_credential",
            appid: config.weixinAppidMobile,
            secret: config.weixinSecretMobile
        }
    }
    return request(data);
})
const getTicket = co.wrap(function *(accessToken){
    let data = {
        url: "https://api.weixin.qq.com/cgi-bin/ticket/getticket",
        method: "get",
        json: true,
        qs: {
            type: "jsapi",
            access_token: accessToken
        }
    }
    return request(data);
})



module.exports = {
    checkLogin: checkLogin,
    getAccessToken:getAccessToken,
    getTicket:getTicket
}
