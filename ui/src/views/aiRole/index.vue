<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item>智慧助手</el-breadcrumb-item>
      <el-breadcrumb-item>人设管理</el-breadcrumb-item>
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
        <el-table-column label="创建时间" prop="create_time" sortable/>
        <el-table-column label="提示词" prop="prompt"/>
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
      <el-form ref="roleForm" :model="form" :rules="rules" label-width="130px">
        <el-form-item label="人设名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入人设名称" :maxlength="25" show-word-limit clearable/>
        </el-form-item>
        <el-form-item label="提示词" prop="prompt">
          <el-input type="textarea" :rows="10" v-model="form.prompt" placeholder="请输入提示词" :maxlength="150"
                    show-word-limit clearable/>
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
import {listRole, getRole, deleteRole, createRole, updateRole} from "@/apis/aiRole/aiRole"

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
          {required: true, message: '人设名称必填', trigger: 'blur'}
        ],
        prompt: [
          {required: true, message: '提示词必填', trigger: 'blur'}
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
      this.$refs['roleForm'].validate(valid => {
        if (!valid) return

        if (this.form.id != null) {
          updateRole(this.form).then(res => {
            if (res.code === 0) {
              this.$message.success('修改成功')
              this.open = false
              this.getList()
            }
          })
        } else {
          createRole(this.form).then(res => {
            if (res.code === 0) {
              this.$message.success('新增成功');
              this.open = false
              this.getList()
            }
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
      listRole(params).then(res => {
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
      this.form = {}
      if (this.$refs['roleForm']) {
        this.$refs['roleForm'].resetFields()
      }
    },
    handleAdd() {
      this.title = '新增系统人设'
      this.open = true
    },
    handleEdit(row) {
      this.reset()
      const id = row.id || this.ids
      getRole(id).then(response => {
        this.form = response.data
        this.open = true
        this.title = '修改系统人设'
      })
    },
    handleDelete(row) {
      const ids = row.id || this.ids.join(',')
      this.$confirm('确认要删除系统人设编号为' + ids + '的数据项吗？', '提示').then(() => {
        deleteRole(ids).then(res => {
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
