<template>
  <div class="page profile-page">
    <div class="profile-card">
      <div class="profile-header">
        <div class="avatar-large">{{ userInfo.username.charAt(0).toUpperCase() }}</div>
        <div>
          <h2>{{ userInfo.username }}</h2>
          <p class="profile-bio" v-if="userInfo.bio">{{ userInfo.bio }}</p>
        </div>
      </div>

      <div class="tabs">
        <button :class="['tab', { active: activeTab === 'info' }]" @click="activeTab = 'info'">个人信息</button>
        <button :class="['tab', { active: activeTab === 'pwd' }]" @click="activeTab = 'pwd'">修改密码</button>
      </div>

      <form v-if="activeTab === 'info'" @submit.prevent="updateProfile" class="profile-form">
        <div class="form-group">
          <label>昵称</label>
          <input v-model="form.nickname" class="input" placeholder="设置昵称" />
        </div>
        <div class="form-group">
          <label>个人简介</label>
          <textarea v-model="form.bio" class="input" rows="3" placeholder="写点个人介绍"></textarea>
        </div>
        <div class="form-group">
          <label>性别</label>
          <select v-model="form.gender" class="input">
            <option value="">保密</option>
            <option value="男">男</option>
            <option value="女">女</option>
          </select>
        </div>
        <p class="error-text" v-if="infoError">{{ infoError }}</p>
        <button type="submit" class="btn btn-primary" :disabled="infoSubmitting">
          {{ infoSubmitting ? '保存中...' : '保存修改' }}
        </button>
      </form>

      <form v-else @submit.prevent="changePwd" class="profile-form">
        <div class="form-group">
          <label>原密码</label>
          <input v-model="pwdForm.oldPassword" class="input" type="password" placeholder="输入原密码" required />
        </div>
        <div class="form-group">
          <label>新密码</label>
          <input v-model="pwdForm.newPassword" class="input" type="password" placeholder="输入新密码（至少6位）" required minlength="6" />
        </div>
        <p class="error-text" v-if="pwdError">{{ pwdError }}</p>
        <button type="submit" class="btn btn-primary" :disabled="pwdSubmitting">
          {{ pwdSubmitting ? '修改中...' : '修改密码' }}
        </button>
      </form>

      <div class="logout-area">
        <button class="btn btn-danger" @click="handleLogout">退出登录</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getUserInfo, updateUserInfo, updatePassword } from '@/api/user'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const { userInfo, updateUserInfo: updateStore, logout } = useUserStore()

const activeTab = ref('info')

const form = ref({ nickname: '', bio: '', gender: '' })
const infoError = ref('')
const infoSubmitting = ref(false)

const pwdForm = ref({ oldPassword: '', newPassword: '' })
const pwdError = ref('')
const pwdSubmitting = ref(false)

function handleLogout() {
  logout()
  router.push('/')
}

async function updateProfile() {
  infoError.value = ''
  infoSubmitting.value = true
  try {
    const data = {}
    if (form.value.nickname) data.nickname = form.value.nickname
    if (form.value.bio) data.bio = form.value.bio
    if (form.value.gender) data.gender = form.value.gender
    const res = await updateUserInfo(data)
    updateStore(res.data)
  } catch (e) {
    infoError.value = e.response?.data?.detail || '保存失败'
  } finally {
    infoSubmitting.value = false
  }
}

async function changePwd() {
  pwdError.value = ''
  if (pwdForm.value.newPassword.length < 6) {
    pwdError.value = '新密码长度至少6位'
    return
  }
  pwdSubmitting.value = true
  try {
    await updatePassword(pwdForm.value.oldPassword, pwdForm.value.newPassword)
    pwdForm.value = { oldPassword: '', newPassword: '' }
  } catch (e) {
    pwdError.value = e.response?.data?.detail || '修改密码失败'
  } finally {
    pwdSubmitting.value = false
  }
}

onMounted(() => {
  if (userInfo.value) {
    form.value = {
      nickname: userInfo.value.nickname || '',
      bio: userInfo.value.bio || '',
      gender: userInfo.value.gender || ''
    }
  }
})
</script>

<style scoped>
.profile-page {
  padding-top: calc(var(--header-height) + 16px);
}

.profile-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: 28px 24px;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--color-border);
}

.avatar-large {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--color-primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 700;
  flex-shrink: 0;
}

.profile-bio {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin-top: 4px;
}

.tabs {
  display: flex;
  gap: 0;
  margin-bottom: 20px;
  border-bottom: 1px solid var(--color-border);
}

.tab {
  padding: 10px 20px;
  font-size: 15px;
  color: var(--color-text-secondary);
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
}
.tab.active {
  color: var(--color-primary);
  border-bottom-color: var(--color-primary);
}

.profile-form {
  max-width: 400px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 14px;
  color: var(--color-text-secondary);
  margin-bottom: 6px;
  font-weight: 500;
}

.logout-area {
  margin-top: 32px;
  padding-top: 20px;
  border-top: 1px solid var(--color-border);
}
</style>
