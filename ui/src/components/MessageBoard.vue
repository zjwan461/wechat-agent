<template>
  <div>
    <!-- Form -->
    <el-dialog :title="title" :visible.sync="visible">
      <el-form :model="form" >
        <el-form-item label="">
          <el-input type="textarea" v-model="form.log" autocomplete="off" rows="25" @input="autoScroll"></el-input>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'MessageBoard',
  props: {
    title: {
      type: String,
      default: '消息面板'
    },
    visible: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      form: {
        log: ''
      },
    }
  },
  methods: {
    autoScroll() {
      this.$nextTick(() => {
        const textarea = this.$refs.messageInput.$el.querySelector('textarea');
        if (textarea) {
          textarea.scrollTop = textarea.scrollHeight;
        }
      });
    },
    appendInfo(line) {
      this.visible = true
      this.form.log += "\n" + line
    },
  }
}
</script>


<style scoped>

</style>
