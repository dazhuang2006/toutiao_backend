import request from './request'

export function login(username, password) {
  return request.post('/user/login', { username, password })
}

export function register(username, password) {
  return request.post('/user/register', { username, password })
}

export function getUserInfo() {
  return request.get('/user/info')
}

export function updateUserInfo(data) {
  return request.put('/user/update', data)
}

export function updatePassword(oldPassword, newPassword) {
  return request.put('/user/update_password', { oldPassword, newPassword })
}
