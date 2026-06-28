import { reactive, computed } from 'vue'

const state = reactive({
  token: localStorage.getItem('token') || null,
  userInfo: JSON.parse(localStorage.getItem('userInfo') || 'null')
})

export function useUserStore() {
  const isLoggedIn = computed(() => !!state.token)
  const token = computed(() => state.token)
  const userInfo = computed(() => state.userInfo)

  function setLogin(token, userInfo) {
    state.token = token
    state.userInfo = userInfo
    localStorage.setItem('token', token)
    localStorage.setItem('userInfo', JSON.stringify(userInfo))
  }

  function updateUserInfo(userInfo) {
    state.userInfo = userInfo
    localStorage.setItem('userInfo', JSON.stringify(userInfo))
  }

  function logout() {
    state.token = null
    state.userInfo = null
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }

  return { isLoggedIn, token, userInfo, setLogin, updateUserInfo, logout }
}
