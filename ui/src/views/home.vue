<template>
  <el-container class="home-container">
    <el-header class="header">
      <!-- 头部导航区域 -->
      <div>
        <img src="../assets/logo.png" width="30" alt>
        <span>微信助手管理平台</span>
      </div>
      <el-dropdown @command="handleCommand">
        <div class="el-dropdown-link">
          <img src="../assets/logo.png" alt width="30">
          <i class="el-icon-arrow-down el-icon--right"/>
        </div>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="setting">
            设 置
          </el-dropdown-item>
          <el-dropdown-item command="logout">
            退 出
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <!-- <el-button >退出</el-button> -->
    </el-header>
    <el-container>
      <!-- 左侧菜单栏区域 -->
      <el-aside :width="asideWidth">
        <el-tooltip effect="dark" content="点击展开或折叠" placement="right-start" :hide-after="1000">
          <div class="toggle-button" @click="toggoleCollapse">
            |||
          </div>
        </el-tooltip>
        <el-menu background-color="#393D49" text-color="#fff" active-text-color="#21A0FE" unique-opened
                 :collapse-transition="false" :collapse="collapse" router :default-active="active"
                 @select="handleSelect">
          <el-menu-item index="/home">
            <i class="el-icon-s-home"></i>
            <span slot="title">系统监控</span>
          </el-menu-item>
          <el-menu-item v-if="item.children === undefined" v-for="(item) in menuData" :key="item.id" :index="item.href">
            <i :class="item.icon"/>
            <span>{{ item.title }}</span>
          </el-menu-item>
          <el-submenu v-if="item.children" v-for="(item) in menuData" :key="item.id" :index="item.id + ''">
            <template slot="title">
              <i :class="item.icon"/>
              <span>{{ item.title }}</span>
            </template>
            <el-menu-item v-for="(child) in item.children" :key="child.id" :index="child.href">
              <template slot="title">
                <i :class="child.icon"/>
                <span>{{ child.title }}</span>
              </template>
            </el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>
      <el-container>
        <el-main>
          <router-view/>
        </el-main>
        <el-footer>
          <span>&copy;zjwan461/wechat_agent</span>
        </el-footer>
      </el-container>
    </el-container>
  </el-container>
</template>

<script>

import {getNav, logout} from '../apis/home'

export default {
  name: 'Home',
  data() {
    return {
      log: '',
      collapse: false,
      asideWidth: '200px',
      menuData: [],
      active: ''
    }
  },
  created() {
    this.getMenuTree()
    this.active = window.sessionStorage.getItem('menu-active-path') ? window.sessionStorage.getItem('menu-active-path') : '/home';
  },
  methods: {
    handleSelect(index, indexPath) {
      window.sessionStorage.setItem('menu-active-path', index)
      this.active = index
    },
    handleCommand(command) {
      if (command === 'setting') {
        this.$router.push({path: '/setting'})
      } else if (command === 'logout') {
        this.$confirm('确定要退出吗？', '系统提示').then(() => {
          logout().then(res => {
            sessionStorage.removeItem('Authorization')
            sessionStorage.removeItem('menu-active-path')
            this.$router.push('/login')
          })
        }).catch(() => {
        })
      }
    },
    getMenuTree() {
      getNav().then(res => {
        this.menuData = res.data
      })
    },
    // 点击按钮，切换菜单折叠与展开
    toggoleCollapse() {
      this.collapse = !this.collapse
      this.asideWidth = this.collapse ? '64px' : '200px'
    },
  }
};
</script>

<style lang="less" scoped>
.el-header {
  background-color: #393d49;
}

.el-aside {
  background-color: #393d49;

  .el-menu {
    border-right: none;
  }
}

.el-main {
  background-color: #eaedf1;
}

.el-footer {
  background-color: #fff;
}

.home-container {
  height: 100%;
}

.header {
  display: flex;
  justify-content: space-between;
  color: #fff;
  margin-left: 0px;
  align-items: center;

  div {
    display: flex;
    align-items: center;

    span {
      margin-left: 20px;
    }
  }
}

.toggle-button {
  background-color: #4a5064;
  color: #fff;
  font-size: 10px;
  line-height: 24px;
  text-align: center;
  letter-spacing: 0.2em;
  cursor: pointer;
}

.el-dropdown-link {
  color: #fff;
  cursor: pointer;

  img {
    width: 35px;
    border-radius: 50%;
  }
}
</style>
