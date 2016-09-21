'use strict'
/**
* @author: ke.wu
* @create_time: 2016-06-28 10:39:28
* @file_name: config.js
* @description: 配置文件
 **/

module.exports = {
  // node server 访问数据源的 IP
  host: 'http://localhost:9527',
  staticHost: 'http://online.polycn.com:9528',
  templatePath: '../static/templates/',
  port: 8004,
  // weixin 登录相关 web
  weixinAccessToken: 'https://api.weixin.qq.com/sns/oauth2/access_token',
  weixinAppid: 'wx6528c82cfdb6e6ae',
  weixinSecret: 'e4532ab343b86610f4fca277ef8d1543',
  weixinUserInfo: 'https://api.weixin.qq.com/sns/userinfo',
  weixinQrConnect: 'https://open.weixin.qq.com/connect/qrconnect',
  weixinRedirectUrl: 'http://online.polycn.com/weixin/oauth2',
  // weixin  登录相关 mobile
  weixinAppidMobile: 'wxc74a0c042c6dc1d7',
  weixinSecretMobile: '2d289bf9a8421d9f42db1916e03088af',
  weixinRedirectUrlMobile: 'http://online.polycn.com/weixin/oauth2_mobile',
  weixinAuthorize: 'https://open.weixin.qq.com/connect/oauth2/authorize',
  // 测试脚本用的 IP
  testHost: 'http://127.0.0.1:8888',
  debug: true
}
