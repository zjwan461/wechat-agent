import request from '../common/request'

export function getYzm(t) {
  return request({
    url: '/api/base/yzm?t=' + t,
    method: 'get'
  })
}

export function getSysInfo() {
  return request({
    url: '/api/base/sys-info',
    method: 'get'
  })
}

export function login(data) {
  return request({
    url: '/api/auth/login',
    method: 'post',
    data: data
  })
}

export function gitRepo(){
  return request({
    url: '/api/base/git-repo',
    method: 'get'
  })
}
