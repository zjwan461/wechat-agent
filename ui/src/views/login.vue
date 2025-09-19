<template>
  <div class="loginContent">
    <div class="loginArea">
      <div class="loginLogo">
        <span>微信智能助手</span>
      </div>
      <!-- 表单登录区域 -->
      <el-form ref="loginForm" label-width="0px" class="loginForm" :model="loginForm" :rules="rules">
        <el-form-item prop="username">
          <el-input v-model="loginForm.username" prefix-icon="el-icon-user-solid" placeholder="账号"/>
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="loginForm.password" prefix-icon="el-icon-lock" placeholder="密码" type="password"/>
        </el-form-item>
        <el-form-item prop="yzm">
          <el-row>
            <el-col :span="18">
              <el-input v-model="loginForm.yzm" prefix-icon="el-icon-info" placeholder="验证码"/>
            </el-col>
            <el-col :span="6">
              <img :src="this.yzmImg" style="width: 100px; padding: 0 5px;" @click="getYzm">
            </el-col>
          </el-row>
        </el-form-item>
        <el-form-item class="btns">
          <el-button type="primary" @click="submitForm('loginForm')">
            登录
          </el-button>
          <el-button type="info" @click="resetForm('loginForm')">
            重置
          </el-button>
        </el-form-item>
        <div style="">
          <a :href="githubUrl" target="_blank" style="color: #01AAED">
            <svg t="1741331388471" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
                 p-id="5122" width="32" height="32">
              <path
                d="M512 85.333333C276.266667 85.333333 85.333333 276.266667 85.333333 512a426.410667 426.410667 0 0 0 291.754667 404.821333c21.333333 3.712 29.312-9.088 29.312-20.309333 0-10.112-0.554667-43.690667-0.554667-79.445333-107.178667 19.754667-134.912-26.112-143.445333-50.133334-4.821333-12.288-25.6-50.133333-43.733333-60.288-14.933333-7.978667-36.266667-27.733333-0.554667-28.245333 33.621333-0.554667 57.6 30.933333 65.621333 43.733333 38.4 64.512 99.754667 46.378667 124.245334 35.2 3.754667-27.733333 14.933333-46.378667 27.221333-57.045333-94.933333-10.666667-194.133333-47.488-194.133333-210.688 0-46.421333 16.512-84.778667 43.733333-114.688-4.266667-10.666667-19.2-54.4 4.266667-113.066667 0 0 35.712-11.178667 117.333333 43.776a395.946667 395.946667 0 0 1 106.666667-14.421333c36.266667 0 72.533333 4.778667 106.666666 14.378667 81.578667-55.466667 117.333333-43.690667 117.333334-43.690667 23.466667 58.666667 8.533333 102.4 4.266666 113.066667 27.178667 29.866667 43.733333 67.712 43.733334 114.645333 0 163.754667-99.712 200.021333-194.645334 210.688 15.445333 13.312 28.8 38.912 28.8 78.933333 0 57.045333-0.554667 102.912-0.554666 117.333334 0 11.178667 8.021333 24.490667 29.354666 20.224A427.349333 427.349333 0 0 0 938.666667 512c0-235.733333-190.933333-426.666667-426.666667-426.666667z"
                fill="#000000" p-id="5123"></path>
            </svg>
          </a>
          <a :href="giteeUrl" target="_blank" style="color: #01AAED;margin: 0 20px">
            <svg t="1741331433921" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
                 p-id="6147" width="32" height="32">
              <path
                d="M512 512m-494.933333 0a494.933333 494.933333 0 1 0 989.866666 0 494.933333 494.933333 0 1 0-989.866666 0Z"
                fill="#C71D23" p-id="6148"></path>
              <path
                d="M762.538667 457.045333h-281.088a24.4736 24.4736 0 0 0-24.439467 24.405334v61.098666c-0.034133 13.5168 10.922667 24.439467 24.405333 24.439467h171.1104c13.5168 0 24.439467 10.922667 24.439467 24.439467v12.219733a73.3184 73.3184 0 0 1-73.3184 73.3184h-232.209067a24.439467 24.439467 0 0 1-24.439466-24.439467v-232.174933a73.3184 73.3184 0 0 1 73.3184-73.3184h342.152533c13.482667 0 24.405333-10.922667 24.439467-24.439467l0.034133-61.098666a24.405333 24.405333 0 0 0-24.405333-24.439467H420.352a183.296 183.296 0 0 0-183.296 183.296V762.538667c0 13.482667 10.922667 24.439467 24.405333 24.439466h360.516267a164.9664 164.9664 0 0 0 165.000533-165.000533v-140.526933a24.439467 24.439467 0 0 0-24.439466-24.439467z"
                fill="#FFFFFF" p-id="6149"></path>
            </svg>
          </a>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
import {Date} from 'core-js'
import {getYzm, getSysInfo, login, gitRepo} from '../apis/login'


export default {
  data() {
    return {
      giteeUrl: '#',
      githubUrl: '#',
      loadingInstance: undefined,
      appInfo: undefined,
      loginForm: {
        username: '',
        password: '',
        yzm: ''
      },
      yzmImg: '',
      rules: {
        username: [
          {required: true, message: '请输入账号', trigger: 'blur'},
          {min: 3, max: 14, message: '长度在 3 到 14 个字符', trigger: 'blur'}
        ],
        password: [
          {required: true, message: '请输入密码', trigger: 'blur'},
          {min: 3, max: 16, message: '长度在 3 到 16 个字符', trigger: 'blur'}
        ]
      }
    }
  },
  mounted() {
    let _self = this
    document.onkeydown = function (e) {
      let key = window.event.keyCode
      if (key === 13) {
        _self.submitForm('loginForm')
      }
    }
    this.getGitRepo()
    this.getSysInfo()
  },
  methods: {
    getGitRepo() {
      gitRepo().then(res => {
        this.giteeUrl = res.data.giteeUrl
        this.githubUrl = res.data.githubUrl
      })
    },
    getSysInfo() {
      getSysInfo().then(res => {
        if (res.data !== null) {
          this.appInfo = res.data
          sessionStorage.setItem('appInfo', JSON.stringify(this.appInfo))
          this.getYzm()
        } else {
          this.$router.push('/register')
        }
      })
    },
    getYzm() {
      if (this.appInfo) {
        getYzm(new Date()).then(res => {
          this.yzmImg = res.data
        })
      }
    },
    submitForm(formName) {
      if (this.appInfo) {
        this.$refs[formName].validate(valid => {
          if (!valid) return
          login(this.loginForm)
            .then(res => {
              if (res.code === 0) {
                let bearerToken = res.data
                if (bearerToken.indexOf('Bearer') === -1) {
                  this.$message.error('非法的token')
                  return false
                }
                sessionStorage.setItem('Authorization', bearerToken.substring(7))
                this.$message({
                  message: '登录成功，页面即将跳转...',
                  type: 'info'
                })
                var that = this
                setTimeout(function () {
                  that.$router.push({path: '/home'})
                }, 1000)
              } else {
                this.getYzm()
              }
            })
            .catch(err => {
              console.log('err', err)
            })
        })
      }
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    }
  }
}
</script>

<style lang="less" scoped>
.loginContent {
  background-image: url("../assets/imgs/login-background.jpg");
  background-size: 100% 100%; /* 宽度和高度都拉伸至容器的100% */
  background-repeat: no-repeat; /* 防止图片重复 */
  background-position: center; /* 图片居中显示 */
  width: 100%;
  height: 100%;
}

.loginArea {
  width: 450px;
  height: 400px;
  background: #fff;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  border-radius: 3px;

  .loginLogo {
    width: 300px;
    height: 100px;
    padding: 20px;
    position: absolute;
    text-align: center;
    left: 50%;
    transform: translate(-50%, 0%);
    background: #fff;

    img {
      width: 20%;
      height: 60%;
    }

    span {
      font-size: 35px;
      padding: 10px;
      font-family: 'Courier New';
    }
  }
}

.loginForm {
  position: absolute;
  bottom: 0;
  width: 100%;
  top: 25%;
  padding: 0 20px;
  box-sizing: border-box;
}

.btns {
  display: flex;
  justify-content: flex-end;
}
</style>
