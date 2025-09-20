import request from '@/common/request'

export function listAgent(params) {
  return request({
    url: '/api/agent/list',
    method: 'get',
    params
  })
}

export function getAgent(id) {
  return request({
    url: '/api/agent/' + id,
    method: 'get'
  })
}
