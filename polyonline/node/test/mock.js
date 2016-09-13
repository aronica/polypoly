'use strict'
/**
* @author: ke.wu
* @create_time: 2016-06-28 12:08:52
* @file_name: mock.js
* @description: 
 **/

const rp = require('request-promise')


module.exports = data => {
  // handle url and object
  if (typeof data === 'string' || typeof data === 'object') {
    console.log('[mock] test data is: %s', JSON.stringify(data))
    rp(data).then(function(res) {
      console.log('========== BEGIN ==========')
      console.log(res)
      console.log('========== END ==========')
    })
  // error
  } else {
    console.log('[mock] ERROR: %o', data)
  }
  return
}
