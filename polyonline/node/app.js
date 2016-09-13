'use strict'
const koa = require('koa')
const router = require('koa-router')()
const logger = require('koa-logger')
const koaBody = require('koa-body')
const staticFile = require('koa-static')
const compress = require('koa-compress')
const dir = require('path')
const config = require('./config/config')

// local module
const handlers = require('./service/http_page')
const services = require('./service/http_service')
const login = require('./util/login')

// koa server
const app = koa()
const port = config.port

// koa middleware
app.use(compress({
  filter: function (content_type) {
    return /text|image|javascript/i.test(content_type)
  },
  threshold: 1024,
  flush: require('zlib').Z_SYNC_FLUSH
}))
app.use(logger())
// 资源文件缓存 12 小时
app.use(staticFile(dir.resolve('../static/'), {
  maxage: 1000 * 60 * 60 * 12
}))
// 不能放到 router 下面，why? 好问题。
app.use(router.routes())

// 验证是否是移动端的中间件
app.use(function *(next) {
  let isMobile = false
  let userAgent = this.request.header['user-agent'].toLowerCase()
  if (userAgent.search(/android|iphone|ipad|windows\ phone/) >= 0) {
    isMobile = true
  }
  console.log('ip of the client: %s', this.request.ip)
  console.log('check whether the client is mobile: %s', isMobile)
  this.isMobile = isMobile
  yield next
})

// 验证是否登录中间件
app.use(function *(next) {
  let openid = this.cookies.get('openid')
  let url = this.request.url
  let userInfo, isLogged

  if (openid) {
    userInfo = yield login['checkLogin'](openid)
  }

  if (userInfo && userInfo.resultCode === 200) {
    isLogged = true
    this.isLogged = true
    this.openid = openid
    this.userInfo = userInfo.result
  } else {
    this.isLogged = false
    isLogged = false
    this.openid = ''
    this.userInfo = ''
  }
  console.log('check whether the visitor is logged: %s', this.isLogged)
  this.cookies.set('url', url)
  yield next
})

/*
 * route for web page and service
 * '*.html' for pages
 * '*' for interfaces
 * */
// 首页
router.get('/index.html', handlers.index)
router.get('/', handlers.index)
// 所有项目页
// 项目巡览页
router.get('/projects.html', handlers.projects)
// 单个项目页
router.get('/project.html', handlers.project)
// 单户型评价页
router.get('/comment.html', handlers.comment)
// 所有户型页
router.get('/houses.html', handlers.houses)
// 个人页面
router.get('/personal.html', handlers.personal)
// 关于保利页面
router.get('/about.html', handlers.about)
router.get('/export.html', handlers['export'])

// 过滤器
router.get('/filter/structurelist', services.structureList)
router.get('/filter/propertylist', services.propertyList)

// 提交评论
router.post('/comment', koaBody(), services.comment)

// 微信登录相关的请求
router.get('/login/weixin', services.loginWX)
router.get('/weixin/oauth2', services.weixinOauth2)
router.get('/weixin/oauth2_mobile', services.weixinOauth2Mobile)

// test.html
router.get('/test.html', handlers.test)

// start server
app.listen(port)
console.log('server starts at %d', port)
