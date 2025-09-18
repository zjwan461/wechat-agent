import request from '../common/request'

export function getSysInfo() {
    return request({
        url: '/api/sys-info',
        method: 'get'
    })
}