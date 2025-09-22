<template>
  <div class="registerContent">
    <div class="registerArea">
      <el-card>
        <h1 class="registerHeader">应用初始化</h1>
        <el-form
          ref="registerForm"
          :model="registerForm"
          label-width="120px"
          class="registerForm"
          :rules="rules"
        >
          <el-form-item
            label="用户名"
            prop="username"
          >
            <el-input
              v-model="registerForm.username"  placeholder="请输入用户名"
              type="text"
            />
          </el-form-item>
          <el-form-item
            label="密码"
            prop="password"
          >
            <el-input
              v-model="registerForm.password" placeholder="请输入密码"
              type="password"
            />
          </el-form-item>
          <el-form-item
            label="二次密码"
            prop="rePwd"
          >
            <el-input
              v-model="registerForm.rePwd" placeholder="请输入密码"
              type="password"
            />
          </el-form-item>
          <el-form-item
            label="邮箱"
            prop="email"
          >
            <el-input
              v-model="registerForm.email" placeholder="请输入邮箱"
              type="email"
            />
          </el-form-item>
          <el-form-item
            label="微信安装目录"
            prop="wechat_install_path"
          >
            <el-input
              v-model="registerForm.wechat_install_path" placeholder="微信的安装目录（Wexin.exe的绝对路径，如：F:\software\Weixin\Weixin.exe）"
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
import {register} from '@/apis/register'

export default {
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
        wechat_install_path: [
          {required: true, message: '请输入微信安装目录', trigger: 'blur'}
        ]
      }
    }
  },
  methods: {
    onSubmit(value) {
      this.$refs[value].validate(valid => {
        if (!valid) return
        register(this.registerForm).then(response => {
          if (response.code === 0) {
            this.$message.success('注册成功,即将返回登录页')
            this.$router.push('/login')
          }
        })
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
  width: 800px;
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
