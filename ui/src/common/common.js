import {Loading, Message, Notification} from 'element-ui'

export function copy(value) {
  const input = document.createElement('input')
  input.setAttribute('readonly', 'readonly')
  input.setAttribute('value', value)
  document.body.appendChild(input)
  input.setSelectionRange(0, 9999)
  input.select()
  document.execCommand('copy')
  document.body.removeChild(input)
  Message({
    message: '已拷贝',
    type: 'success'
  })
}

export function getRequestBodyStr(obj) {
  let reqStr = ''
  for (let key in obj) {
    reqStr += key + '=' + obj[key] + '&'
  }
  return reqStr
}

export function getRequestBodyJson(obj) {
  return JSON.stringify(obj)
}

export async function fetchFluxData(uri, callback, signal) {
  try {
    const response = await fetch(uri, {signal});
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    // console.log(response)
    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')
    while (true) {
      const {done, value} = await reader.read()
      if (done) {
        break
      }
      const chunk = decoder.decode(value);
      const data = chunk.replace('data:', '')
      if (callback) {
        callback(data);
      }
    }
  } catch (error) {
    console.error('Error fetching data:', error)
  }
}

export function startLoading(text) {
  if (!text) {
    text = '拼命加载中...'
  }
  return Loading.service({
    lock: true,
    text: text,
    background: 'rgba(255,255,255,0.5)',
    target: document.querySelector('body')
  });
}

export function endLoading(loading) { //  关闭加载动画
  if (loading) {
    loading.close()
  }
}

export function showNotice(title, msg, type) {
  Notification({
    title: title,
    message: msg,
    type: type,
    duration: 5000
  })
}

export function getDateString() {
  const now = new Date();

// 获取各个时间组件
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0'); // 月份从0开始
  const day = String(now.getDate()).padStart(2, '0');
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');

// 格式1：YYYY-MM-DD-HH:MM:SS
//   return `${year}-${month}-${day}-${hours}-${minutes}-${seconds}`
  return year + '-' + month + '-' + day + '-' + hours + '-' + minutes + '-' + seconds
}

export function closestMultipleOf8(num) {
  const remainder = num % 8;

  if (remainder === 0) {
    return num; // 已经是 8 的倍数
  } else if (remainder <= 4) {
    return num - remainder; // 向下取整
  } else {
    return num + (8 - remainder); // 向上取整
  }
}
