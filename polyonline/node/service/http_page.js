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
    variableEnd: '=}'
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
    //cityList.result.cities = cityList.result.cities.splice(0,0,'全部城市')
    let propertyList = yield renderer['getProperyList'](city)
    let propertyListDetail = propertyList.result.properties
    for(let i = 0;i<propertyListDetail.length;i++){
      let item = propertyListDetail[i]
      if(item.location && item.location.indexOf("（")>0){
        item.location = item.location.substring(0,item.location.indexOf("（"))
      }
      if(item.description && item.description.length>250){
        item.description = item.description.substring(0,250)
        item.desc_more = true;
      }
    }
    this.body = nj.render('index/projects.html', {
      isMobile: this.isMobile,
      cityList: cityList.result.cities,
      propertyList: propertyListDetail,
      userInfo: this.userInfo,
      city: city || '全部城市',
      datetime: dt(),
      page:'list'
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

      let item = structureList.result.property
      if(item.location && item.location.indexOf("（")>0){
        item.location = item.location.substring(0,item.location.indexOf("（"))
      }

      this.body = nj.render('index/project.html', {
      isMobile: this.isMobile,
        property: item,
        structures: structureList.result.structures,
        filterList: filterList.result,
        userInfo: this.userInfo,
        areaValue: area_value,
        structureValue: structure_value,
        datetime: dt(),
        page:'detail'
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
      type: this.request.query.type || 0,
      titles:'公司简介'
    })
  },
  'export': function *(next) {
    yield next

    this.body = nj.render('index/export.html', {
      isMobile: this.isMobile,
      staticAddress: config.staticHost
    })
  },
  president: function* (next) {
    yield next
    this.body = nj.render('index/president.html', {
      isMobile: this.isMobile,
      type: this.request.query.type || 1,
      titles:'领导致辞'
    })
  },
  company: function* (next) {
    yield next
    this.body = nj.render('index/company.html', {
      isMobile: this.isMobile,
      type: this.request.query.type || 1,
      titles:'保利集团'
    })
  },
  platform: function* (next) {
    yield next
    this.body = nj.render('index/platform.html', {
      isMobile: this.isMobile,
      type: this.request.query.type || 1,
      titles:'保利云产品平台',
      menu:'关于我们'
    })
  },
  honor: function* (next) {
    yield next
    this.body = nj.render('index/honor.html', {
      isMobile: this.isMobile,
      type: this.request.query.type || 1,
      titles:'企业荣誉',
      menu:'关于我们',
      pn: this.request.query.pn || 1,
      year: this.request.query.year ||"",
      total:2
    })
  },
  journey: function* (next) {
    yield next
    this.body = nj.render('index/journey.html', {
      isMobile: this.isMobile,
      type: this.request.query.type || 1,
      titles:'发展历程',
      menu:'关于我们',
      pn: this.request.query.pn || 1,
      year: this.request.query.year ||"",
      total:2
    })
  }
}

