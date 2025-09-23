<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item>智慧助手</el-breadcrumb-item>
      <el-breadcrumb-item>助手维护</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-form :inline="true" v-model="search">
        <el-form-item label="名称">
          <el-input v-model="search.name" placeholder="请输入名称" clearable/>
        </el-form-item>
        <el-form-item label="好友名称">
          <el-input v-model="search.nickname" placeholder="请输入好友名称" clearable/>
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
        <el-table-column label="好友昵称" prop="nickname"/>
        <el-table-column label="聊天类型" prop="chat_type">
          <template slot-scope="scope">
            <el-tag :type="scope.row.chat_type === 'PRIVATE' ? 'success' : 'primary'">{{ scope.row.chat_type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="助手类型" prop="type">
          <template slot-scope="scope">
            <el-tag :type="scope.row.type === 'SIMPLE' ? 'success' : 'primary'">{{ scope.row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="回复群组" prop="reply_group"/>
        <el-table-column label="AI模型" prop="model"/>
        <el-table-column label="人设" prop="ai_role"/>
        <el-table-column label="状态" prop="status" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === '已停止' ? 'danger' : 'success'">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
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
      <el-form ref="agentForm" :model="form" :rules="rules" label-width="130px">
        <el-form-item label="助手名" prop="name">
          <el-input v-model="form.name" placeholder="请输入助手名称" :maxlength="25" show-word-limit clearable/>
        </el-form-item>
        <el-form-item label="好友昵称" prop="nickname">
          <el-input v-model="form.nickname" placeholder="请输入好友昵称" :maxlength="50" show-word-limit clearable/>
        </el-form-item>
        <el-form-item label="聊天类型" prop="chat_type">
          <el-radio-group v-model="form.chat_type">
            <el-radio label="PRIVATE">私聊</el-radio>
            <el-radio label="GROUP">群聊</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="助手类型" prop="type">
          <el-radio-group v-model="form.type">
            <el-radio label="SIMPLE">指定回复</el-radio>
            <el-radio label="AI">AI回复</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="回复群组" prop="reply_group" v-show="form.type ==='SIMPLE'">
          <el-select v-model="form.reply_group" multiple :multiple-limit="3">
            <el-option v-for="(item,index) in reply_groups" :key="index" :value="item" :label="item"/>
          </el-select>
        </el-form-item>
        <el-form-item label="AI模型" prop="model_id" v-show="form.type === 'AI'">
          <el-select v-model="form.model_id">
            <el-option v-for="item in model_list" :key="item.id" :value="item.id" :label="item.name"/>
          </el-select>
        </el-form-item>
        <el-form-item label="人设" prop="ai_role_id" v-show="form.type === 'AI'">
          <el-select v-model="form.ai_role_id">
            <el-option v-for="item in ai_role_list" :key="item.id" :value="item.id" :label="item.name"/>
          </el-select>
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
import {listAgent, getAgent, createAgent, updateAgent, deleteAgent} from '@/apis/agent/agent'
import {listModel} from '@/apis/model/model'
import {listRole} from '@/apis/aiRole/aiRole'
import {getReplyGroups} from '@/apis/reply/reply'

export default {
  data() {
    return {
      model_list: [],
      ai_role_list: [],
      reply_groups: [],
      ids: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      open: false,
      title: '',
      rules: {
        name: [
          {required: true, message: '助手名称必填', trigger: 'blur'}
        ],
        nickname: [
          {required: true, message: '好友昵称必填', trigger: 'blur'}
        ],
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
    getReplyGroups() {
      getReplyGroups().then(res => {
        if (res.code === 0) {
          this.reply_groups = res.data
        }
      })
    },
    getModels() {
      listModel({page: 1, page_size: 10000}).then(res => {
        if (res.code === 0) {
          this.model_list = res.rows
        }
      })
    },
    getAiRoles() {
      listRole({page: 1, page_size: 10000}).then(res => {
        if (res.code === 0) {
          this.ai_role_list = res.rows
        }
      })
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.id)
      this.single = selection.length !== 1
      this.multiple = !selection.length
    },
    submitForm() {
      this.$refs['agentForm'].validate(valid => {
        if (!valid) return
        if (this.form.reply_group) {
          this.form.reply_group = this.form.reply_group.join(',')
        }
        if (this.form.id != null) {
          updateAgent(this.form).then(res => {
            if (res.code === 0) {
              this.$message.success('修改成功')
              this.open = false
              this.getList()
            }
          })
        } else {
          createAgent(this.form).then(res => {
            if (res.code === 0) {
              this.$message.success('新增成功')
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
      listAgent(params).then(res => {
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
        chat_type: 'PRIVATE',
        type: 'AI'
      }
      if (this.$refs['agentForm']) {
        this.$refs['agentForm'].resetFields()
      }
    },
    handleAdd() {
      this.title = '新增助手'
      this.open = true
      this.reset()
      this.getModels()
      this.getAiRoles()
      this.getReplyGroups()
    },
    handleEdit(row) {
      this.reset()
      const id = row.id || this.ids
      getAgent(id).then(response => {
        this.form = response.data
        this.open = true
        this.title = '修改AI智能体'
      })
      this.getModels()
      this.getAiRoles()
      this.getReplyGroups()
    },
    handleDelete(row) {
      const ids = row.id || this.ids
      this.$confirm('确认要删除助手编号为' + ids + '的数据项吗？', '提示').then(() => {
        deleteAgent(ids).then(res => {
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

  },
}
</script>

<style lang="less" scoped>
.setting-form {
  padding: 0 20px;
}
</style>
