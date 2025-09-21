import request from '@/common/request'

export function listReply(params) {
  return request({
    url: '/api/reply/list',
    method: 'get',
    params: params
  })
}

export function getReply(id) {
  return request({
    url: '/api/reply/' + id,
    method: 'get'
  })
}

export function createReply(data) {
  return request({
    url: '/api/reply/create',
    method: 'post',
    data: data
  })
}

export function updateReply(data) {
  return request({
    url: '/api/reply/update',
    method: 'put',
    data: data
  })
}

export function deleteReply(ids) {
  return request({
    url: '/api/reply/delete/' + ids,
    method: 'delete'
  })
}
