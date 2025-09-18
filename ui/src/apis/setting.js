import request from '../common/request'

export function getSetting() {
    return request({
        url: '/api/setting',
        method: 'get'
    })
}