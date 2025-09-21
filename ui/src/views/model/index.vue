<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item>智慧助手</el-breadcrumb-item>
      <el-breadcrumb-item>AI模型维护</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-form :inline="true" v-model="search">
        <el-form-item label="名称">
          <el-input v-model="search.name" placeholder="请输入名称"/>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="getList">查询</el-button>
        </el-form-item>
      </el-form>
      <el-row :gutter="10" class="mb8">
        <el-col :span="1.5">
          <el-button type="primary" plain icon="el-icon-plus" size="mini" @click="handleAdd">新增</el-button>
        </el-col>
        <el-col :span="1.5">
          <el-button type="success" plain icon="el-icon-edit" size="mini" :disabled="single" @click="handleEdit">修改
          </el-button>
        </el-col>
        <el-col :span="1.5">
          <el-button type="danger" plain icon="el-icon-delete" size="mini" :disabled="multiple" @click="handleDelete">删除
          </el-button>
        </el-col>
      </el-row>
      <el-table :data="list" v-loading="loading" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" align="center"/>
        <el-table-column label="ID" prop="id"/>
        <el-table-column label="名称" prop="name"/>
        <el-table-column label="提供商" prop="provider">
          <template slot-scope="scope">
            <el-tag :type="scope.row.provider === 'Ollama' ? 'primary' : 'success'">{{ scope.row.provider }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="base_url" prop="base_url"/>
        <el-table-column label="max_tokens" prop="max_tokens"/>
        <el-table-column label="api_key" prop="api_key"/>
        <el-table-column label="temperature" prop="temperature"/>
        <el-table-column label="top_k" prop="top_k"/>
        <el-table-column label="top_p" prop="top_p"/>
        <el-table-column label="创建时间" prop="create_time" sortable/>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="text" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="text" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total">
      </el-pagination>

    </el-card>
    <el-dialog :title="title" :visible.sync="open" width="800px" append-to-body>
      <el-form ref="modelForm" :model="form" :rules="rules" label-width="130px">
        <el-form-item label="模型名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入模型名称" :maxlength="50"
                    show-word-limit clearable/>
        </el-form-item>
        <el-form-item label="提供商" prop="provider">
          <el-select v-model="form.provider">
            <el-option value="Ollama" label="Ollama"/>
            <el-option value="Open_AI" label="Open_AI"/>
          </el-select>
        </el-form-item>
        <el-form-item label="base_url" prop="base_url">
          <el-input v-model="form.base_url" placeholder="请输入base url" clearable/>
        </el-form-item>
        <el-form-item label="api_key" prop="api_key">
          <el-input v-model="form.api_key" placeholder="请输入api_key" clearable/>
        </el-form-item>
        <el-form-item label="max_tokens" prop="max_tokens">
          <el-input-number :step="100" v-model="form.max_tokens" placeholder="请输入max_tokens"
                           clearable/>
        </el-form-item>
        <el-form-item label="temperature" prop="temperature">
          <el-input-number :min="0.01" :max="1.0" :step="0.1" v-model="form.temperature" placeholder="请输入temperature"
                           clearable/>
        </el-form-item>
        <el-form-item label="top_k" prop="top_k">
          <el-input-number :min="10" :max="100" :step="1" v-model="form.top_k" placeholder="请输入top_k"
                           clearable/>
        </el-form-item>
        <el-form-item label="top_p" prop="top_p">
          <el-input-number :min="0.01" :max="1.0" :step="0.1" v-model="form.top_p" placeholder="请输入top_p"
                           clearable/>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {listModel, getModel, deleteModel, createModel, updateModel} from '@/apis/model/model'

export default {
  data() {
    return {
      ids: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      open: false,
      title: '',
      rules: {
        name: [
          {required: true, message: '名称必填', trigger: 'blur'}
        ],
        provider: [
          {required: true, message: '模型提供商必填', trigger: 'change'}
        ],
        base_url: [
          {required: true, message: 'base_url必填', trigger: 'blur'}
        ],
        temperature: [
          {required: true, message: 'temperature必填', trigger: 'blur'}
        ],
        max_tokens: [
          {required: true, message: 'max_tokens必填', trigger: 'blur'}
        ]
      },
      form: {},
      loading: false,
      search: {},
      list: [],
      currentPage: 1,
      pageSize: 10,
      total: 0
    }
  },
  created() {
    this.getList()
  },
  methods: {
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.id)
      this.single = selection.length !== 1
      this.multiple = !selection.length
    },
    submitForm() {
      this.$refs['modelForm'].validate(valid => {
        if (!valid) return

        if (this.form.id != null) {
          updateModel(this.form).then(res => {
            this.$message.success('修改成功')
            this.open = false
            this.getList()
          })
        } else {
          createModel(this.form).then(res => {
            this.$message.success('新增成功')
            this.open = false
            this.getList()
          })
        }
      })
    },
    getList() {
      const params = {
        page: this.currentPage,
        page_size: this.pageSize,
        ...this.search
      }
      this.loading = true
      listModel(params).then(res => {
        this.loading = false
        this.list = res.rows
        this.total = res.total
      })
    },
    cancel() {
      this.reset()
      this.open = false
    },
    reset() {
      this.form = {
        provider: 'Open_AI',
        temperature: 0.7,
        max_tokens: 2048
      }
      this.$refs['modelForm'].resetFields()
    },
    handleAdd() {
      this.title = '新增预设回复'
      this.open = true
    },
    handleEdit(row) {
      this.reset()
      const id = row.id || this.ids
      getModel(id).then(response => {
        this.form = response.data
        this.open = true
        this.title = '修改预设回复'
      })
    },
    handleDelete(row) {
      const ids = row.id || this.ids.join(',')
      this.$confirm('确认要删除预设回复编号为' + ids + '的数据项吗？', '提示').then(() => {
        deleteModel(ids).then(res => {
          this.getList()
        })
      }).catch(() => {
      })
    },
    handleSizeChange(size) {
      this.pageSize = size
      this.getList()
    },
    handleCurrentChange(currentPage) {
      this.currentPage = currentPage
      this.getList()
    }

  }
}
</script>

<style lang="less" scoped>
.setting-form {
  padding: 0 20px;
}
</style>
