<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item>设置</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-row>
        <el-col :span="12">
          <el-form :model="settings" :rules="rules" class="setting-form" label-width="160px">
            <el-form-item>
              <el-button type="primary" @click="save">提交</el-button>
            </el-form-item>
          </el-form>
        </el-col>
        <el-col :span="12">
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import { getSetting } from "../apis/setting";

export default {
  data() {
    return {
      rules: {
        model_save_dir: [
          { required: true, message: '模型保存目录必填', trigger: 'blur' }
        ]
      },
      auto_open_log_window: true,
      settings: {
       
      }
    }
  },
  created() {
    this.getSettings()
  },
  methods: {
    save() {

    },
    getSettings() {
      getSetting().then(res => {

      })
    },

  },
}
</script>

<style lang="less" scoped>
.setting-form {
  padding: 0 20px;
}
</style>
