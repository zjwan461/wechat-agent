<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item>设置</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-row>
        <el-col :span="12">
          <el-form ref="setting" :model="setting" :rules="rules" class="setting-form" label-width="160px">
            <el-form-item label="模型保存目录" prop="model_save_dir">
              <el-input v-model="setting.model_save_dir" placeholder="模型保存目录"></el-input>
            </el-form-item>
            <el-form-item label="代理地址" prop="proxy_host">
              <el-input v-model="setting.proxy_host" placeholder="代理地址"></el-input>
            </el-form-item>
            <el-form-item label="代理端口" prop="proxy_port">
              <el-input-number :min="1000" :max="65535" :step="1" v-model="setting.proxy_port"
                               placeholder="代理端口"></el-input-number>
            </el-form-item>
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
import {getSetting, updateSetting} from "../apis/setting";

export default {
  data() {
    return {
      rules: {
        model_save_dir: [
          {required: true, message: '模型保存目录必填', trigger: 'blur'}
        ]
      },
      setting: {}
    }
  },
  created() {
    this.getSettings()
  },
  methods: {
    save() {
      this.$refs['setting'].validate(valid => {
        if (!valid) return
        updateSetting(this.setting).then(res => {
          if (res.code === 0) {
            this.$message.success('保存成功')
          }
        })
      })
    },
    getSettings() {
      getSetting().then(res => {
        this.setting = res.data
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
