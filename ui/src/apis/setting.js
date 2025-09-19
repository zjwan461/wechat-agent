import request from '../common/request'

export function getSetting() {
  return request({
    url: '/api/setting',
    method: 'get'
  })
}

export function updateSetting(data) {
  return request({
    url: '/api/setting',
    method: 'post',
    data: data
  })
}
