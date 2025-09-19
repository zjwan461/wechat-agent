import request from '../common/request'

export function register(data) {
  return request({
    url: '/api/register',
    method: 'post',
    data: data
  })
}
