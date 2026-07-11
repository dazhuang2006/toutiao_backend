<template>
  <div class="page profile-page">
    <div class="profile-header">
      <div class="profile-avatar">
        <img v-if="userInfo?.avatar" :src="userInfo.avatar" />
        <span v-else class="avatar-letter">{{ userInfo?.username?.[0] || "U" }}</span>
      </div>
      <h2 class="profile-name">{{ userInfo?.username || "用户" }}</h2>
      <p v-if="userInfo?.bio" class="profile-bio">{{ userInfo.bio }}</p>
    </div>

    <div class="profile-section">
      <h3 class="section-label">个人信息</h3>
      <div class="form-group">
        <label class="form-label">昵称</label>
        <input v-model="form.nickname" class="input" placeholder="设置昵称" />
      </div>
      <div class="form-group">
        <label class="form-label">个人简介</label>
        <input v-model="form.bio" class="input" placeholder="介绍一下自己" />
      </div>
      <button class="btn btn-primary" @click="handleUpdate" :disabled="updating">
        {{ updating ? "保存中..." : "保存修改" }}
      </button>
    </div>

    <div class="profile-section">
      <h3 class="section-label">修改密码</h3>
      <div class="form-group">
        <label class="form-label">旧密码</label>
        <input v-model="pwdForm.oldPassword" type="password" class="input" placeholder="输入旧密码" />
      </div>
      <div class="form-group">
        <label class="form-label">新密码</label>
        <input v-model="pwdForm.newPassword" type="password" class="input" placeholder="输入新密码（至少6位）" minlength="6" />
      </div>
      <button class="btn btn-outline" @click="handleChangePwd" :disabled="changingPwd">
        {{ changingPwd ? "修改中..." : "修改密码" }}
      </button>
    </div>

    <div class="profile-section logout-section">
      <button class="btn btn-danger logout-btn" @click="handleLogout">退出登录</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue"
import { useRouter } from "vue-router"
import { getUserInfo, updateUserInfo, updatePassword } from "@/api/user"
import { useUserStore } from "@/stores/user"

const router = useRouter()
const { userInfo, updateUserInfo: storeUpdate, logout } = useUserStore()

const form = reactive({ nickname: "", bio: "" })
const pwdForm = reactive({ oldPassword: "", newPassword: "" })
const updating = ref(false)
const changingPwd = ref(false)

onMounted(() => {
  if (userInfo.value) {
    form.nickname = userInfo.value.nickname || ""
    form.bio = userInfo.value.bio || ""
  }
})

async function handleUpdate() {
  updating.value = true
  try {
    const res = await updateUserInfo({ nickname: form.nickname, bio: form.bio })
    storeUpdate(res.data)
  } catch (e) { console.error(e) }
  finally { updating.value = false }
}

async function handleChangePwd() {
  changingPwd.value = true
  try {
    await updatePassword(pwdForm.oldPassword, pwdForm.newPassword)
    pwdForm.oldPassword = ""
    pwdForm.newPassword = ""
  } catch (e) { console.error(e) }
  finally { changingPwd.value = false }
}

function handleLogout() {
  logout()
  router.push("/")
}
</script>

<style scoped>
.profile-header { text-align: center; padding: 24px 0 20px; }
.profile-avatar { width: 72px; height: 72px; border-radius: 50%; margin: 0 auto 12px; overflow: hidden; background: var(--primary-soft); display: flex; align-items: center; justify-content: center; }
.profile-avatar img { width: 100%; height: 100%; object-fit: cover; }
.avatar-letter { font-size: 28px; font-weight: 700; color: var(--primary); }
.profile-name { font-size: 20px; font-weight: 700; color: var(--text); margin-bottom: 4px; }
.profile-bio { font-size: 14px; color: var(--text-muted); }
.profile-section { background: var(--surface); border-radius: var(--radius-md); padding: 20px; margin-bottom: 12px; box-shadow: var(--shadow-sm); }
.section-label { font-size: 15px; font-weight: 600; color: var(--text); margin-bottom: 16px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
.form-group { margin-bottom: 14px; }
.form-label { display: block; font-size: 13px; font-weight: 500; color: var(--text-secondary); margin-bottom: 4px; }
.logout-section { margin-top: 24px; }
.logout-btn { width: 100%; padding: 10px; font-size: 15px; }
</style>
