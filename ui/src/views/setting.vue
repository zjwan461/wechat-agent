<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item>设置</el-breadcrumb-item>
      <el-breadcrumb-item>系统设置</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-row>
        <el-col :span="12">
          <el-form ref="setting" :model="setting" :rules="rules" class="setting-form" label-width="160px">
            <el-form-item label="模型保存目录" prop="model_save_dir">
              <el-input v-model="setting.model_save_dir" placeholder="模型保存目录"></el-input>
            </el-form-item>
            <el-form-item label="微信安装目录" prop="wechat_install_path">
              <el-input v-model="setting.wechat_install_path" placeholder="微信安装绝对路径"></el-input>
            </el-form-item>
            <el-form-item label="微信版本" prop="wechat_version">
              <el-select v-model="setting.wechat_version" clearable>
                <el-option label="V3" value=V3>V3</el-option>
                <el-option label="V4" value=V4>V4</el-option>
              </el-select>
            </el-form-item>
            <el-form-item
              label="微信昵称"
              prop="my_wechat_names"
            >
              <el-select
                v-model="setting.my_wechat_names"
                multiple
                filterable
                allow-create
                default-first-option
                placeholder="你的微信昵称，可配置多个，考虑到在群聊中可能拥有不同的昵称">
                <el-option
                  v-for="item in setting.my_wechat_names"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="代理地址" prop="proxy_host">
              <el-input v-model="setting.proxy_host" placeholder="代理地址"></el-input>
            </el-form-item>
            <el-form-item label="代理端口" prop="proxy_port">
              <el-input-number :max="65535" :step="1" v-model="setting.proxy_port"
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
        ],
        wechat_install_path: [
          {required: true, message: '请输入微信安装目录', trigger: 'blur'}
        ],
        my_wechat_names: [
          {required: true, message: '请输入你的微信昵称', trigger: 'blur'}
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
        let req = {...this.setting}
        if (req.my_wechat_names) {
          req.my_wechat_names = req.my_wechat_names.join(',')
        }
        updateSetting(req).then(res => {
          if (res.code === 0) {
            if (this.setting.wechat_version === 'V4') {
              this.$message.warning('4.0+版本存在一些bug，建议使用3.9+版本微信')
            } else {
              this.$message.success('保存成功')
            }
          }
        });
      })
    },
    getSettings() {
      getSetting().then(res => {
        let data = res.data
        if (data.my_wechat_names) {
          data.my_wechat_names = data.my_wechat_names.split(',')
        }
        this.setting = data
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
