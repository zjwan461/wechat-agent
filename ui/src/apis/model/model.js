import request from '@/common/request'

export function listModel(params) {
  return request({
    url: '/api/model/list',
    method: 'get',
    params: params
  })
}

export function getModel(id) {
  return request({
    url: '/api/model/' + id,
    method: 'get'
  })
}

export function createModel(data) {
  return request({
    url: '/api/model/create',
    method: 'post',
    data: data
  })
}

export function updateModel(data) {
  return request({
    url: '/api/model/update',
    method: 'put',
    data: data
  })
}

export function deleteModel(ids) {
  return request({
    url: '/api/model/delete/' + ids,
    method: 'delete'
  })
}
