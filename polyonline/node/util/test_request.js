'use strict'

const req = require('./request')
const request = require('request')
const co = require('co')

const data = {
  uri: 'httP://127.0.0.1:9527/property/list',
  method: 'GET',
  json: true,
  qs: {
    city: '佛山'
  }
}

let b  = co(function *() {
  let ret = yield req(data)
  console.log('--------')
  console.log(ret)
  console.log('--------')
  return ret
}).catch(function(e) {
  console.log(e)
})
console.log(b)


let test = co.wrap(function *(options) {
  return req(options)
})

test(data).then(function(rt) {
console.log('======')
console.log(rt)
console.log('======')
})


co(function *() {
  let a = yield ret()

console.log("++++++")
  console.log(a)
console.log("++++++")
})


let r = co.wrap(function *(city) {
  let res
  request(data, function(r, e) {
    console.log(e.body)
    res = e.body
  })
  return yield res
})

var fn = co.wrap(function* (val) {
      return yield request(data)
});

fn(data).then(function (val) {
   console.log('casdcasdcsda', val)
});
co(function* () {
      var result = yield request(data)
    console.log(result)
        return result;
}).then(function (value) {
      console.log(value);
}, function (err) {
      console.error(err.stack);
});
