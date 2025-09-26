<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item>历史消息</el-breadcrumb-item>
      <el-breadcrumb-item>消息列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-form :inline="true" v-model="search">
        <el-form-item label="智慧助手">
          <el-select v-model="search.agent_id" clearable>
            <el-option v-for="item in agent_list" :key="item.id" :label="item.name" :value="item.id"/>
          </el-select>
        </el-form-item>
        <el-form-item label="聊天窗口">
          <el-input v-model="search.nickname" placeholder="聊天窗口名" clearable/>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="getList">查询</el-button>
        </el-form-item>
      </el-form>
      <el-row :gutter="10" class="mb8">
        <el-col :span="1.5">
          <el-button type="primary" plain icon="el-icon-info" size="mini" :disabled="single" @click="handleInfo">详情
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
        <el-table-column label="智慧助手" prop="agent"/>
        <el-table-column label="聊天窗口" prop="nickname"/>
        <el-table-column label="聊天类型" prop="chat_type">
          <template slot-scope="scope">
            <el-tag :type="scope.row.chat_type === '私聊' ? 'success' : 'primary'">{{ scope.row.chat_type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="智能体类型" prop="agent_type">
          <template slot-scope="scope">
            <el-tag :type="scope.row.agent_type === '指定回复' ? 'success' : 'primary'">{{ scope.row.agent_type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="消息内容" prop="content">
          <template slot-scope="scope">
            <div>{{ scope.row.content.substring(0, 50) + '...' }}</div>
          </template>
        </el-table-column>
        <el-table-column label="回信人" prop="create_by"/>
        <el-table-column label="创建时间" prop="create_time" sortable/>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="text" @click="handleInfo(scope.row)">详情</el-button>
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
      <el-form ref="form" :model="form" label-width="130px">
        <el-form-item label="智慧助手" prop="agent">
          <el-input v-model="form.agent" readonly/>
        </el-form-item>
        <el-form-item label="助手类型" prop="agent_type">
          <el-input v-model="form.agent_type" readonly/>
        </el-form-item>
        <el-form-item label="聊天类型" prop="chat_type">
          <el-input v-model="form.chat_type" readonly/>
        </el-form-item>
        <el-form-item label="回信人" prop="create_by">
          <el-input v-model="form.create_by" readonly/>
        </el-form-item>
        <el-form-item label="消息内容" prop="content">
          <el-input type="textarea" :rows="10" v-model="form.content" readonly/>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import {listHistory, getHistory, deleteHistory} from '@/apis/history/history'
import {listAgent} from '@/apis/agent/agent'

export default {
  data() {
    return {
      agent_list: [],
      ids: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      loading: false,
      search: {},
      open: false,
      title: '',
      form: {},
      list: [],
      currentPage: 1,
      pageSize: 10,
      total: 0
    }
  },
  created() {
    this.getList()
    this.getAgentList()
  },
  methods: {
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.id)
      this.single = selection.length !== 1
      this.multiple = !selection.length
    },
    getList() {
      const params = {
        page: this.currentPage,
        page_size: this.pageSize,
        ...this.search
      }
      this.loading = true
      listHistory(params).then(res => {
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
      if (this.$refs['form']) {
        this.$refs['form'].resetFields()
      }
    },
    handleInfo(row) {
      this.reset()
      const id = row.id || this.ids
      getHistory(id).then(res => {
        if (res.code === 0) {
          this.form = res.data
          this.open = true
          this.title = '查看消息详情'
        }
      })
    },
    handleDelete(row) {
      const ids = row.id || this.ids.join(',')
      this.$confirm('确认要删除历史记录编号为' + ids + '的数据项吗？', '提示').then(() => {
        deleteHistory(ids).then(res => {
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
    },
    getAgentList() {
      listAgent({ page: 1, page_size: 1000 }).then(res => {
        this.agent_list = res.rows
      })
    }

  }
}
</script>

<style lang="less" scoped>
.setting-form {
  padding: 0 20px;
}
</style>
