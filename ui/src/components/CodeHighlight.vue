<template>
  <div class="code-highlight-container">
    <div class="code-header" v-if="showHeader">
      <div class="code-lang">{{ language.toUpperCase() }}</div>
      <div class="code-actions">
        <el-button
          size="mini"
          type="text"
          icon="el-icon-document-copy"
          @click="copyCode"
          :disabled="!code"
        >复制
        </el-button>
        <el-button size="mini" type="text" @click="editSystem" icon="el-icon-edit" v-if="showEditSys">编辑器中打开</el-button>
        <el-button
          size="mini"
          :type="isEditing ? 'success' : 'info'"
          @click="toggleEditMode"
        >
          <i :class="isEditing ? 'el-icon-check' : 'el-icon-edit'"></i>
          {{ isEditing ? '保存' : '编辑' }}
        </el-button>
      </div>
    </div>
    <pre
      ref="codeBlock"
      :class="['hljs', currentTheme]"
      :style="{maxHeight: maxHeight}"
      v-show="!isEditing"
    >
      <code :class="language" v-html="formattedCode"></code>
    </pre>
    <el-input
      type="textarea"
      :rows="10"
      v-model="editedCode"
      :autosize="{ minRows: 10, maxRows: 20 }"
      v-show="isEditing"
      @input="onCodeChange"
      class="edit-code-area"
    ></el-input>
  </div>
</template>

<script>
import hljs from 'highlight.js/lib/core';
import 'highlight.js/styles/github.css';

// 注册需要支持的语言
import javascript from 'highlight.js/lib/languages/javascript';
import python from 'highlight.js/lib/languages/python';
import java from 'highlight.js/lib/languages/java';
import html from 'highlight.js/lib/languages/xml'; // HTML 使用 xml 模式
import css from 'highlight.js/lib/languages/css';
import sql from 'highlight.js/lib/languages/sql';
import json from 'highlight.js/lib/languages/json';
import typescript from 'highlight.js/lib/languages/typescript';
import bash from 'highlight.js/lib/languages/bash';

hljs.registerLanguage('javascript', javascript);
hljs.registerLanguage('python', python);
hljs.registerLanguage('java', java);
hljs.registerLanguage('html', html);
hljs.registerLanguage('css', css);
hljs.registerLanguage('sql', sql);
hljs.registerLanguage('json', json);
hljs.registerLanguage('typescript', typescript);
hljs.registerLanguage('bash', bash);

export default {
  name: 'CodeHighlight',
  props: {
    code: {
      type: String,
      default: ''
    },
    language: {
      type: String,
      default: 'javascript'
    },
    theme: {
      type: String,
      default: 'github'
    },
    showHeader: {
      type: Boolean,
      default: true
    },
    maxHeight: {
      type: String,
      default: '500px'
    },
    expand: {
      type: Boolean,
      default: true
    },
    showEditSys: {
      type: Boolean,
      default: false
    },
    filePath: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      currentTheme: this.theme,
      isExpanded: this.expand,
      isEditing: false,
      originCode: this.code,
      editedCode: this.code,
      hightlight: false
    }
  },
  computed: {
    formattedCode() {
      // console.log(this.code)
      if (!this.originCode) return '';

      // 处理代码缩进
      const lines = this.originCode.split('\n');
      if (lines.length <= 1) return this.originCode;

      // 找到第一个非空行
      let firstNonEmptyLine = null;
      for (const line of lines) {
        if (line.trim() !== '') {
          firstNonEmptyLine = line;
          break;
        }
      }

      if (!firstNonEmptyLine) return this.originCode;

      // 计算缩进空格数
      const indentMatch = firstNonEmptyLine.match(/^\s+/);
      const indent = indentMatch ? indentMatch[0] : '';

      // 移除共同缩进
      if (indent) {
        const indentRegex = new RegExp(`^${indent}`);
        return lines.map(line => line.replace(indentRegex, '')).join('\n');
      }

      return this.originCode;
    }
  },
  mounted() {
    this.highlightCode()
  },
  watch: {
    language() {
      this.highlightCode();
    },
    isEditing(val) {
      if (!val) {
        this.highlightCode();
      }
    },
    editedCode() {
      // this.highlightCode()
    },

  },
  methods: {
    editSystem() {
      
    },
    highlightCode() {
      if (!this.$refs.codeBlock) return;

      const codeElement = this.$refs.codeBlock.querySelector('code');
      if (!codeElement) return;

      this.originCode = hljs.highlightAuto(this.editedCode).value
    },

    async copyCode() {
      if (!this.originCode) return;

      try {
        // 使用 Clipboard API
        await navigator.clipboard.writeText(this.editedCode);
        // this.copyMessage = '复制成功';
        this.$message.success("复制成功")
      } catch (error) {
        // 备选方案：使用 textarea
        const textarea = document.createElement('textarea');
        textarea.value = this.editedCode;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);

        this.$message.success("复制成功")
      }
    },

    toggleExpand() {
      this.isExpanded = !this.isExpanded;
    },
    toggleEditMode() {
      if (this.isEditing) {
        // 保存编辑
        this.$emit('save', this.editedCode);
      }
      this.isEditing = !this.isEditing;
    },
    onCodeChange() {
      this.$emit('change', this.editedCode);
    }
  }
};
</script>

<style scoped>
.code-highlight-container {
  margin: 15px 0;
}

.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.code-lang {
  font-weight: bold;
  color: #606266;
  font-family: 'Source Code Pro', Consolas, monospace;
}

.code-actions {
  display: flex;
  gap: 10px;
}

pre {
  margin: 0 !important;
  padding: 1em !important;
  overflow: auto !important;
  border-radius: 4px !important;
  font-size: 14px !important;
  line-height: 1.5 !important;
  tab-size: 4 !important;
}

/* 代码折叠样式 */
pre {
  max-height: 400px;
  transition: max-height 0.3s ease;
}

pre.expanded {
  max-height: none;
}

.edit-code-area .el-textarea__inner {
  font-family: Consolas, Monaco, 'Andale Mono', monospace;
  font-size: 14px;
  line-height: 1.5;
  tab-size: 4;
  white-space: pre;
  word-wrap: normal;
  overflow-x: auto;
}

code {
  font-family: 'Source Code Pro', Consolas, monospace !important;
}

/* 隐藏未选中的主题 */
</style>
