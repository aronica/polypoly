'use strict'
/**
 * @author: Ke Wu
 * @createdTime: 2016-08-12 17:14:06
 * @fileName: renderer.js
 * @description: 获取渲染模版的数据用
 **/

const request = require('../util/request')
const config = require('../config/config')
const co = require('co')

const getBanner = co(function *() {
  let data = {
    uri: config.host + '/index',
    method: 'GET',
    json: true
  }

  return request(data)
})

const getCityList = co(function *() {
  let data = {
    uri: config.host + '/city/list',
    method: 'GET',
    json: true
  }

  return request(data)
})

const getProperyList = co.wrap(function *(city) {
  let data = {
    uri: config.host + '/property/list',
    method: 'GET',
    json: true,
    qs: {
      city: city
    }
  }

  let ret = request(data)
  return ret
})

const getStructureList = co.wrap(function *(propertyId, area_value, structure_value) {
  let roomCount, toiletCount, hallCount, lowerLimit, upperLimit
  if (area_value === '全部' || !area_value) {
    lowerLimit = ''
    upperLimit = ''
  } else {
    area_value = area_value.split(',')
    lowerLimit = area_value[0]
    upperLimit = area_value[1]
  }

  if (structure_value === '全部' || !structure_value) {
    roomCount = ''
    toiletCount = ''
    hallCount = ''
  } else {
    structure_value = structure_value.split(',')
    roomCount = structure_value[0]
    hallCount = structure_value[1]
    toiletCount = structure_value[2]
  }

  let data = {
    uri: config.host + '/structure/list',
    method: 'GET',
    json: true,
    qs: {
      property_id: propertyId,
      room_count: roomCount || '',
      toilet_count: toiletCount || '',
      hall_count: hallCount || '',
      lower_limit: lowerLimit || '',
      upper_limit: upperLimit || ''
    }
  }

  return request(data)
})

const getStructureFilter = co.wrap(function *(propertyId) {
  let data = {
    uri: config.host + '/structure/filter',
    method: 'GET',
    json: true
  }

  if (propertyId) {
    data.qs = { property_id: propertyId }
  }

  return request(data)
})

const getStructureDetail = co.wrap(function *(structureId, openid, propertyId) {
  let data = {
    uri: config.host + '/structure/detail',
    method: 'GET',
    json: true,
    qs: {
      structure_id: structureId,
      property_id: propertyId
    }
  }

  if (openid) {
    data.qs.openid = openid
  }

  return request(data)
})

const getPersonalStructure = co.wrap(function(openid) {
  let data = {
    uri: config.host + '/user/structure/get',
    method: 'GET',
    json: true,
    qs: {
      openid: openid
    }
  }

  return request(data)
})

module.exports = {
  getBanner: getBanner,
  getCityList: getCityList,
  getProperyList: getProperyList,
  getStructureList: getStructureList,
  getStructureFilter: getStructureFilter,
  getStructureDetail: getStructureDetail,
  getPersonalStructure: getPersonalStructure
}
