import axios from 'axios'
import router from '../router/index'
import {startLoading, endLoading, getRequestBodyJson} from './common'
import {Message} from 'element-ui'

const service = axios.create({
  timeout: 60000
})

let loading = null
service.interceptors.request.use(request => {
  loading = startLoading()
  request.headers['Content-Type'] = 'application/json'
  const token = sessionStorage.getItem('Authorization')
  if (token) {
    request.headers['Authorization'] = 'Bearer ' + token
  }
  request.data = getRequestBodyJson(request.data)
  return request
}, error => {
  console.log(error)
  Promise.reject(error)
})

service.interceptors.response.use(response => {
  endLoading(loading)
  if (response.data.code !== 0) {
    Message.error(response.data.msg)
  }
  return response.data
}, (error) => {
  endLoading(loading)
  Message({
    message: error.message,
    type: 'error'
  })
  if (error.response.status === 401) {
    sessionStorage.removeItem('Authorization')
    sessionStorage.removeItem('menu-active-path')
    router.push({
      path: '/login'
    })
  }
  return Promise.reject(error)
})

export default service
