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

export function createAgent(data) {
  return request({
    url: '/api/agent/create',
    method: 'post',
    data: data
  })
}

export function updateAgent(data) {
  return request({
    url: '/api/agent/update',
    method: 'put',
    data: data
  })
}

export function deleteAgent(ids) {
  return request({
    url: '/api/agent/delete/' + ids,
    method: 'delete'
  })
}

export function startAgent(id) {
  return request({
    url: '/api/agent/start/' + id,
    method: 'post'
  })
}
