import request from '../common/request'

export function watchInfo() {
  return request({
    url: '/api/watch/info',
    method: 'get'
  })
}
