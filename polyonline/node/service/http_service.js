'use strict'
/**
* @author: ke.wu
* @create_time: 2016-06-24 11:07:13
* @file_name: http_service.js
* @description: HTTP 服务接口
 **/

const config = require('../config/config')
const request = require('../util/request')
const renderer = require('./renderer')
const querystring = require('querystring')


module.exports = {
  comment: function *() {

    let querydata = this.query
    let structureId = querydata.structure_id
    let propertyId = querydata.property_id
    let uri = config.host + '/comment?structure_id=' + structureId
    let body = this.request.body

    if (propertyId) {
      uri += '&property_id=' + propertyId
    }

    let postData = {
      uri: uri,
      method: 'POST',
      json: true,
      body: {
        comment: body.comment,
        title: body.title,
        phone: body.phone,
        estimated_time: body.estimatedTime
      }
    }

    let openid = this.cookies.get('openid')
    if (openid) {
      postData.body.openid = openid
    }

    this.body = yield request(postData)
  },
  structureList: function *() {
    let qs = this.request.query

    let propertyId = qs.property_id
    let roomCount = qs.room_count
    let toiletCount = qs.toilet_count
    let hallCount = qs.hall_count

    let lowerLimit = qs.lower_limit
    let upperLimit = qs.upper_limit

    let structureList = yield renderer['getStructureList'](propertyId, roomCount, toiletCount, hallCount, lowerLimit, upperLimit)
    this.body = structureList
  },
  propertyList: function *() {
     this.body = 'true'
  },
  loginWX: function *() {
    let isMobile = this.request.query.isMobile
    let qs
    if (isMobile === 'true') {
      qs = querystring.stringify({
        appid: config.weixinAppidMobile,
        redirect_uri: config.weixinRedirectUrlMobile,
        response_type: 'code',
        scope: 'snsapi_userinfo',
        state: 'STATE', // encodeURIComponent FIXME
      })
      this.redirect(config.weixinAuthorize + '?' + qs + '#wechat_redirect')
      this.status = 302
    } else {
      qs = querystring.stringify({
        appid: config.weixinAppid,
        redirect_uri: config.weixinRedirectUrl,
        response_type: 'code',
        scope: 'snsapi_login',
        state: 'STATE', // encodeURIComponent FIXME
      })
      this.redirect(config.weixinQrConnect + '?' + qs)
      this.status = 302
    }
  },
  weixinOauth2: function *() {
    // 微信 redirect 的链接
    let data = {
      uri: config.weixinAccessToken,
      method: 'GET',
      json: true,
      qs: {
        appid: config.weixinAppid,
        secret: config.weixinSecret,
        code: '',
        grant_type: 'authorization_code'
      }
    }

    let qs = this.request.query
    if (qs.code) {
      data.qs.code = qs.code
    }

    let res = yield request(data)
    let userInfoData = {
      uri: config.weixinUserInfo,
      method: 'GET',
      json: true,
      qs: {
        access_token: res.access_token,
        openid: res.openid
      }
    }
    let userInfo = yield request(userInfoData)
    let storeUserInfo = {
      uri: config.host + '/user/weixin/set',
      method: 'POST',
      json: true,
      body: userInfo
    }

    let setRet = yield request(storeUserInfo)

    // cookie 保存 openid TODO
    this.cookies.set('openid', userInfo.openid)
    this.redirect(this.cookies.get('url') || '/index.html')
  },
  weixinOauth2Mobile: function *() {
    // 微信 redirect 的链接
    let data = {
      uri: config.weixinAccessToken,
      method: 'GET',
      json: true,
      qs: {
        appid: config.weixinAppidMobile,
        secret: config.weixinSecretMobile,
        code: '',
        grant_type: 'authorization_code'
      }
    }

    let qs = this.request.query
    if (qs.code) {
      data.qs.code = qs.code
    }
    let res = yield request(data)
    let userInfoData = {
      uri: config.weixinUserInfo,
      method: 'GET',
      json: true,
      qs: {
        access_token: res.access_token,
        openid: res.openid
      }
    }
    let userInfo = yield request(userInfoData)
    let storeUserInfo = {
      uri: config.host + '/user/weixin/set',
      method: 'POST',
      json: true,
      body: userInfo
    }

    let setRet = yield request(storeUserInfo)

    // cookie 保存 openid TODO
    this.cookies.set('openid', userInfo.openid)
    this.redirect(this.cookies.get('url') || '/index.html')
  }
}

