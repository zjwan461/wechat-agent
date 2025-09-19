<template>
  <div class="app-container">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item>系统监控</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row>
      <el-col :span="12" class="card-box">
        <el-card>
          <div slot="header"><span><i class="el-icon-cpu"></i> CPU</span></div>
          <div class="el-table el-table--enable-row-hover el-table--medium">
            <table cellspacing="0" style="width: 100%;">
              <thead>
              <tr>
                <th class="el-table__cell is-leaf">
                  <div class="cell">属性</div>
                </th>
                <th class="el-table__cell is-leaf">
                  <div class="cell">值</div>
                </th>
              </tr>
              </thead>
              <tbody>
              <tr>
                <td class="el-table__cell is-leaf">
                  <div class="cell">核心数</div>
                </td>
                <td class="el-table__cell is-leaf">
                  <div class="cell" v-if="server.cpu">{{ server.cpu.cores }}</div>
                </td>
              </tr>
              <tr>
                <td class="el-table__cell is-leaf">
                  <div class="cell">系统使用率</div>
                </td>
                <td class="el-table__cell is-leaf">
                  <div class="cell" v-if="server.cpu">{{ server.cpu.use_percent }}</div>
                </td>
              </tr>
              <tr>
                <td class="el-table__cell is-leaf">
                  <div class="cell">当前空闲率</div>
                </td>
                <td class="el-table__cell is-leaf">
                  <div class="cell" v-if="server.cpu">{{ server.cpu.free_percent }}</div>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
        </el-card>
      </el-col>

      <el-col :span="12" class="card-box">
        <el-card>
          <div slot="header"><span><i class="el-icon-tickets"></i> 内存</span></div>
          <div class="el-table el-table--enable-row-hover el-table--medium">
            <table cellspacing="0" style="width: 100%;">
              <thead>
              <tr>
                <th class="el-table__cell is-leaf">
                  <div class="cell">属性</div>
                </th>
                <th class="el-table__cell is-leaf">
                  <div class="cell">内存</div>
                </th>
              </tr>
              </thead>
              <tbody>
              <tr>
                <td class="el-table__cell is-leaf">
                  <div class="cell">总内存</div>
                </td>
                <td class="el-table__cell is-leaf">
                  <div class="cell" v-if="server.memory">{{ server.memory.total_memory }}</div>
                </td>
              </tr>
              <tr>
                <td class="el-table__cell is-leaf">
                  <div class="cell">已用内存</div>
                </td>
                <td class="el-table__cell is-leaf">
                  <div class="cell" v-if="server.memory">{{ server.memory.used_memory }}</div>
                </td>
              </tr>
              <tr>
                <td class="el-table__cell is-leaf">
                  <div class="cell">剩余内存</div>
                </td>
                <td class="el-table__cell is-leaf">
                  <div class="cell" v-if="server.memory">{{ server.memory.free_memory }}</div>
                </td>
              </tr>
              <tr>
                <td class="el-table__cell is-leaf">
                  <div class="cell">使用率</div>
                </td>
                <td class="el-table__cell is-leaf">
                  <div class="cell" v-if="server.memory">
                    {{ server.memory.memory_percent }}
                  </div>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
        </el-card>
      </el-col>

      <el-col :span="12" class="card-box">
        <el-card>
          <div slot="header"><span><i class="el-icon-cpu"></i> GPU</span></div>
          <div class="el-table el-table--enable-row-hover el-table--medium">
            <table cellspacing="0" style="width: 100%;">
              <thead>
              <tr>
                <th class="el-table__cell is-leaf">
                  <div class="cell">GPU型号</div>
                </th>
                <th class="el-table__cell is-leaf">
                  <div class="cell">显存</div>
                </th>
                <th class="el-table__cell is-leaf">
                  <div class="cell">驱动版本</div>
                </th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="(gpu, index) in server.gpus" :key="index">
                <td class="el-table__cell is-leaf">
                  <div class="cell">{{ gpu.name }}</div>
                </td>
                <td class="el-table__cell is-leaf">
                  <div class="cell">{{ gpu.memory }} GB</div>
                </td>
                <td class="el-table__cell is-leaf">
                  <div class="cell">{{ gpu.driver }}</div>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
        </el-card>
      </el-col>

      <el-col :span="12" class="card-box">
        <el-card>
          <div slot="header">
            <span><i class="el-icon-monitor"></i> 主机信息</span>
          </div>
          <div class="el-table el-table--enable-row-hover el-table--medium">
            <table cellspacing="0" style="width: 100%;">
              <tbody>
              <tr>
                <td class="el-table__cell is-leaf">
                  <div class="cell">主机名称</div>
                </td>
                <td class="el-table__cell is-leaf">
                  <div class="cell" v-if="server.os">{{ server.os.hostname }}</div>
                </td>
                <td class="el-table__cell is-leaf">
                  <div class="cell">操作系统</div>
                </td>
                <td class="el-table__cell is-leaf">
                  <div class="cell" v-if="server.os">{{ server.os.os }}</div>
                </td>
              </tr>
              <tr>
                <td class="el-table__cell is-leaf">
                  <div class="cell">服务器IP</div>
                </td>
                <td class="el-table__cell is-leaf">
                  <div class="cell" v-if="server.os">{{ server.os.ip }}</div>
                </td>
                <td class="el-table__cell is-leaf">
                  <div class="cell">系统架构</div>
                </td>
                <td class="el-table__cell is-leaf">
                  <div class="cell" v-if="server.os">{{ server.os.arch }}</div>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
        </el-card>
      </el-col>

      <el-col :span="24" class="card-box">
        <el-card>
          <div slot="header">
            <span><i class="el-icon-receiving"></i> App信息</span>
          </div>
          <div class="el-table el-table--enable-row-hover el-table--medium">
            <table cellspacing="0" style="width: 100%;">
              <thead>
              <tr>
                <th class="el-table__cell el-table__cell is-leaf">
                  <div class="cell">系统平台</div>
                </th>
                <th class="el-table__cell is-leaf">
                  <div class="cell">系统类型</div>
                </th>
                <th class="el-table__cell is-leaf">
                  <div class="cell">GPU平台</div>
                </th>
                <th class="el-table__cell is-leaf">
                  <div class="cell">App版本</div>
                </th>
              </tr>
              </thead>
              <tbody v-if="server.sysInfo">
              <tr>
                <td class="el-table__cell is-leaf">
                  <div class="cell">{{ server.sysInfo.platform }}</div>
                </td>
                <td class="el-table__cell is-leaf">
                  <div class="cell">{{ server.sysInfo.os_arch }}</div>
                </td>
                <td class="el-table__cell is-leaf">
                  <div class="cell">{{ server.sysInfo.gpu_platform }}</div>
                </td>
                <td class="el-table__cell is-leaf">
                  <div class="cell">{{ server.sysInfo.version }}</div>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import {watchInfo} from '../apis/watch'

export default {
  name: 'Server',
  data() {
    return {
      // 服务器信息
      server: {}
    }
  },
  created() {
    this.getList()
  },
  methods: {
    /** 查询服务器信息 */
    getList() {
      watchInfo().then(res => {
        this.server = res.data
        this.$store.commit('setServerInfo', this.server)
      })
    }
  }
}
</script>
