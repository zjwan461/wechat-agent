import request from '../common/request'

export function initEnv() {
  return request({
    url: '/api/base/init-env',
    method: 'get'
  })
}

export function getNav() {
  return request({
    url: '/api/base/nav',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/api/logout',
    method: 'get'
  })
}
