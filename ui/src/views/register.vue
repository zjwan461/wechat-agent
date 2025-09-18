<template>
  <div class="registerContent">
    <div class="registerArea">
      <el-card>
        <h1 class="registerHeader">应用初始化</h1>
        <el-form
          ref="registerForm"
          :model="registerForm"
          label-width="80px"
          class="registerForm"
          :rules="rules"
        >
          <el-form-item
            label="用户名"
            prop="username"
          >
            <el-input
              v-model="registerForm.username"
              type="text"
            />
          </el-form-item>
          <el-form-item
            label="密码"
            prop="password"
          >
            <el-input
              v-model="registerForm.password"
              type="password"
            />
          </el-form-item>
          <el-form-item
            label="二次密码"
            prop="rePwd"
          >
            <el-input
              v-model="registerForm.rePwd"
              type="password"
            />
          </el-form-item>
          <el-form-item
            label="邮箱"
            prop="email"
          >
            <el-input
              v-model="registerForm.email"
              type="email"
            />
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              @click="onSubmit('registerForm')"
            >
              立即注册
            </el-button>
          </el-form-item>
        </el-form>
        <!--        <a href="javascript:;" style="color: #01AAED" @click="toLogin">前往登录</a>-->
      </el-card>
    </div>
  </div>
</template>

<script>
import {getRequestBodyJson} from '@/common/common'

export default {
  name: 'register',
  data() {
    const rePwd = (rule, value, callback) => {
      if (this.registerForm.password !== value) {
        callback(new Error('两次密码输入不一致'))
      } else {
        callback()
      }
    }
    return {
      registerForm: {},
      rules: {
        username: [
          {required: true, message: '请输入用户名', trigger: 'blur'}
        ],
        password: [
          {required: true, message: '', trigger: 'blur'},
          {min: 6, message: '最少6位密码', trigger: 'blur'}
        ],
        rePwd: [
          {validator: rePwd, trigger: 'blur', required: true}
        ],
        email: [
          {pattern: /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/, trigger: 'blur', required: true}
        ],

      }
    }
  },
  methods: {
    onSubmit(value) {
      this.$refs[value].validate(valid => {
        if (!valid) return
        
      })
    }
  }
}
</script>

<style scoped lang="less">
.registerContent {
  background: #2b4b6b;
  width: 100%;
  height: 100%;
}

.registerArea {
  width: 600px;
  height: 600px;
  position: absolute;
  left: 50%;
  top: 40%;
  transform: translate(-50%, -50%);
  //margin: 200px auto;
  border-radius: 3px;
}

.registerForm {
  padding: 20px 0;
}

.registerHeader {
  text-align: center
}

</style>
