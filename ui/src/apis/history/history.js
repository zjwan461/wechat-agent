import request from '@/common/request'

export function listHistory(params) {
  return request({
    url: '/api/history/list',
    method: 'get',
    params: params
  })
}

export function getHistory(id) {
  return request({
    url: '/api/history/' + id,
    method: 'get'
  })
}

export function deleteHistory(ids) {
  return request({
    url: '/api/history/delete/' + ids,
    method: 'delete'
  })
}
