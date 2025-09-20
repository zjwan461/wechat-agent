import request from '../common/request'

export function register(data) {
  return request({
    url: '/api/auth/register',
    method: 'post',
    data: data
  })
}
