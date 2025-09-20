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
    request.headers['Authorization'] = token
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
}, async error => {
  const originalRequest = error.config
  endLoading(loading)
  if (error.response.status === 401) {
    if (error.response.data.msg === 'Token has expired') {
      try {
        // 1. 获取新的token（示例：调用刷新令牌接口）
        const refreshResponse = await axios.post('/api/auth/refresh-token', getRequestBodyJson({
          refreshToken: sessionStorage.getItem('Authorization')
        }), {
          headers: {
            'Content-Type': 'application/json'
          }
        })
        const newToken = refreshResponse.data.data
        sessionStorage.setItem('Authorization', newToken)

        // 2. 更新原请求的Authorization头
        originalRequest.headers.Authorization = newToken

        // 3. 重新发送请求
        return service(originalRequest)
      } catch (refreshError) {
        console.log(refreshError)
        // 刷新令牌失败，可能需要跳转到登录页
        router.push({
          path: '/login'
        })
        return Promise.reject(refreshError)
      }
    } else {
      Message({
        message: error.response.data.msg || error.message,
        type: 'error'
      })
      sessionStorage.removeItem('Authorization')
      sessionStorage.removeItem('menu-active-path')
      router.push({
        path: '/login'
      })
    }
  } else {
    Message({
      message: error.response.data.msg || error.message,
      type: 'error'
    })
  }
  return Promise.reject(error)
})

export default service
