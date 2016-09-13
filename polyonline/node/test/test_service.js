'use strict'
/**
* @author: ke.wu
* @create_time: 2016-06-28 12:03:08
* @file_name: test_service.js
* @description: 
 **/

const mock = require('./mock')
const config = require('../config/config')


mock(config.testHost + '/updateboard?datetime=20160527')

mock(config.testHost + '/updatediagram?datetime=20160527')

mock(config.testHost + '/update?datetime=20160527')
