<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item>智慧助手</el-breadcrumb-item>
      <el-breadcrumb-item>预设回复</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-form :inline="true" v-model="search">
        <el-form-item label="回复内容">
          <el-input v-model="search.content" placeholder="请输入回复内容"/>
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
        <el-table-column label="回复内容" prop="content"/>
        <el-table-column label="分组" prop="group"/>
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
      <el-form ref="replyForm" :model="form" :rules="rules" label-width="130px">
        <el-form-item label="回复内容" prop="content">
          <el-input type="textarea" :rows="10" v-model="form.content" placeholder="请输入回复内容" :maxlength="150"
                    show-word-limit clearable/>
        </el-form-item>
        <el-form-item label="分组" prop="group">
          <el-input v-model="form.group" placeholder="请输入分组，默认为default" :maxlength="10" show-word-limit
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
import {listReply, getReply, deleteReply, createReply, updateReply} from '@/apis/reply/reply'

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
        content: [
          {required: true, message: '回复内容必填', trigger: 'blur'}
        ],
        group: [
          {required: true, message: '分组必填', trigger: 'blur'}
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
      this.$refs['replyForm'].validate(valid => {
        if (!valid) return

        if (this.form.id != null) {
          updateReply(this.form).then(res => {
            if (res.code === 0) {
              this.$message.success('修改成功')
              this.reset()
              this.getList()
            }
          })
        } else {
          createReply(this.form).then(res => {
            if (res.code === 0) {
              this.$message.success('新增成功')
              this.reset()
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
      listReply(params).then(res => {
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
        content: '',
        group: 'default'
      }
      if (this.$refs['replyForm']) {
        this.$refs['replyForm'].resetFields()
      }
    },
    handleAdd() {
      this.title = '新增预设回复'
      this.open = true
    },
    handleEdit(row) {
      this.reset()
      const id = row.id || this.ids
      getReply(id).then(response => {
        this.form = response.data
        this.open = true
        this.title = '修改预设回复'
      })
    },
    handleDelete(row) {
      const ids = row.id || this.ids.join(',')
      this.$confirm('确认要删除预设回复编号为' + ids + '的数据项吗？', '提示').then(() => {
        deleteReply(ids).then(res => {
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
