import request from '@/common/request';

export function listRole(params) {
  return request({
    url: '/api/aiRole/list',
    method: 'get',
    params: params
  })
}

export function getRole(id) {
  return request({
    url: '/api/aiRole/' + id,
    method: 'get'
  })
}

export function createRole(data) {
  return request({
    url: '/api/aiRole/create',
    method: 'post',
    data: data
  })
}

export function updateRole(data) {
  return request({
    url: '/api/aiRole/update',
    method: 'put',
    data: data
  })
}

export function deleteRole(ids) {
  return request({
    url: '/api/aiRole/delete/' + ids,
    method: 'delete'
  })
}
