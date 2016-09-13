'use strict'
/**
* @author: ke.wu
* @create_time: 2016-06-24 16:24:20
* @file_name: http_page.js
* @description: HTTP 页面
 **/

const nunjucks = require('nunjucks')
const request = require('../util/request')
const config = require('../config/config')
const renderer = require('./renderer')
const co = require('co')
const login = require('../util/login')
const dt = require('../util/datetime')


// nunjucks settings
const tplPath = require('path').resolve(config.templatePath)
// nunjucks 和前端框架 vuejs 冲突，更改 nunjucks 的默认语法
let nj = nunjucks.configure(tplPath, {
  tags: {
    blockStart: '{%',
    blockEnd: '%}',
    variableStart: '{=',
    variableEnd: '=}',
  },
  watch: true
});

// handlers
module.exports = {
  index: function *(next) {
    yield next
    let banner = yield renderer.getBanner

    this.body = nj.render('index/index.html', {
      isMobile: this.isMobile,
      data: banner.result
    })
  },
  test: function* (next) {
    yield next

    this.body = nj.render('index/test.html')
  },
  projects: function* (next) {
    yield next

    let city = this.request.query.city || ''

    let cityList = yield renderer.getCityList
    let propertyList = yield renderer['getProperyList'](city)
    this.body = nj.render('index/projects.html', {
      isMobile: this.isMobile,
      cityList: cityList.result.cities,
      propertyList: propertyList.result.properties,
      userInfo: this.userInfo,
      city: city || '全部城市',
      datetime: dt()
    })
  },
  project: function* (next) {
    yield next
    if (this.isLogged) {
      // 只有登录状态才能走到这个逻辑
      let qs = this.request.query
      let propertyId = qs.property_id
      let area_value = qs.area_value || ''
      let structure_value = qs.structure_value || ''
      let structureList = yield renderer['getStructureList'](propertyId, area_value, structure_value)
      let filterList = yield renderer['getStructureFilter'](propertyId)

      this.body = nj.render('index/project.html', {
      isMobile: this.isMobile,
        property: structureList.result.property,
        structures: structureList.result.structures,
        filterList: filterList.result,
        userInfo: this.userInfo,
        areaValue: area_value,
        structureValue: structure_value,
        datetime: dt()
      })
    } else {
      this.redirect('/login/weixin?isMobile=' + this.isMobile)
      this.status = 302
    }
  },
  houses: function* (next) {
    yield next

    let qs = this.request.query
    let area_value = qs.area_value || ''
    let structure_value = qs.structure_value || ''

    let structureList = yield renderer['getStructureList']('', area_value, structure_value)
    let filterList = yield renderer['getStructureFilter']()

    this.body = nj.render('index/houses.html', {
      isMobile: this.isMobile,
      property: structureList.result.property,
      structures: structureList.result.structures,
      filterList: filterList.result,
      userInfo: this.userInfo,
      areaValue: area_value,
      structureValue: structure_value,
      datetime: dt()
    })
  },
  personal: function* (next) {
    yield next
    if (this.isLogged) {
      // 只有登录状态才能走到这个逻辑
      let personalStructure = yield renderer['getPersonalStructure'](this.openid)
      let result = personalStructure.result

      this.body = nj.render('index/personal.html', {
        isMobile: this.isMobile,
        comment: result ? result.comment : null,
        structure: result ? result.structure : null,
        property: result ? result.property : null,
        userInfo: this.userInfo,
        datetime: dt()
      })
    } else {
      this.redirect('/login/weixin?isMobile=' + this.isMobile)
      this.status = 302
    }
  },
  comment: function* (next) {
    yield next

    let req = this.request
    // 非产品巡览过来的链接都隐藏价格
    let fromHouse = true
    if (req.header.referer) {
      fromHouse = (req.header.referer.indexOf('project.html') === -1)
    }
    let qs = req.query
    let structureId = qs.structure_id
    let propertyId = qs.property_id || ''

    let structureDetail = yield renderer['getStructureDetail'](structureId, this.openid, propertyId)

    this.body = nj.render('index/comment.html', {
      isMobile: this.isMobile,
      structureDetail: structureDetail.result,
      fromHouse: fromHouse,
      userInfo: this.userInfo,
      datetime: dt()
    })
  },
  about: function* (next) {
    yield next
    this.body = nj.render('index/about.html', {
      isMobile: this.isMobile,
      type: this.request.query.type || ''
    })
  },
  'export': function *(next) {
    yield next

    this.body = nj.render('index/export.html', {
      isMobile: this.isMobile,
      staticAddress: config.staticHost
    })
  }
}
