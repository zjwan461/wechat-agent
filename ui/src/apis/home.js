import request from '../common/request'

export function getNav() {
  return request({
    url: '/api/base/nav',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/api/auth/logout',
    method: 'get'
  })
}
