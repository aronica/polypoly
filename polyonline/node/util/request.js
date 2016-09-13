'use strict'
/**
* @author: ke.wu
* @create_time: 2016-07-05 15:15:46
* @file_name: request.js
* @description: 封装的 HTTP 请求方法，用于 generator
 **/

// request promise using in koa
const requestPromise = require('request-promise')

module.exports = requestJson => requestPromise(requestJson).then(res => res)

