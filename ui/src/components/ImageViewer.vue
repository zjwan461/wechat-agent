<template>
  <div class="image-viewer-container">
    <el-dialog
      :visible.sync="dialogVisible"
      title="图片查看器"
      width="80%"
      :close-on-click-modal="false"
      @close="handleClose"
    >
      <template>
        <div class="image-viewer-content" v-if="imageUrl">
          <!-- 工具栏 -->
          <div class="image-viewer-toolbar">
            <el-button icon="el-icon-zoom-in" @click="zoomIn">放大</el-button>
            <el-button icon="el-icon-zoom-out" @click="zoomOut">缩小</el-button>
            <el-button icon="el-icon-refresh-right" @click="rotateRight">右转</el-button>
            <el-button icon="el-icon-refresh-left" @click="rotateLeft">左转</el-button>
            <el-button icon="el-icon-download" @click="saveImg">保存</el-button>
          </div>

          <!-- 图片容器 -->
          <div class="image-wrapper" ref="imageWrapper">
            <img
              :src="imageUrl"
              :style="{
                transform: `scale(${scale}) rotate(${rotate}deg)`,
                transition: 'transform 0.3s'
              }"
              @load="onImageLoad"
              class="viewable-image"
              ref="image"
            >
          </div>
        </div>

        <!-- 加载状态 -->
        <div class="loading-state" v-else>
          <el-loading-spinner></el-loading-spinner>
          <p>等待图片数据...</p>
        </div>
      </template>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'ImageViewer',
  props: {
    // 控制对话框显示/隐藏
    visible: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      dialogVisible: this.visible,
      imageUrl: '',           // 图片 URL
      scale: 1,               // 缩放比例
      rotate: 0,              // 旋转角度
      maxScale: 3,            // 最大缩放比例
      minScale: 0.5,          // 最小缩放比例
      scaleStep: 0.1          // 缩放步长
    };
  },
  watch: {
    // 监听父组件传递的 visible 属性
    visible(val) {
      this.dialogVisible = val;
      if (!val) {
        this.resetViewer();  // 关闭时重置状态
      }
    }
  },
  methods: {
    // 接收 Base64 数据并显示图片
    loadImage(base64Data) {
      // 检查是否包含数据前缀
      if (base64Data.startsWith('data:')) {
        this.imageUrl = base64Data;
      } else {
        this.imageUrl = `data:image/png;base64,${base64Data}`;
      }
    },

    // 图片加载完成事件
    onImageLoad() {
      // 重置变换
      this.scale = 1;
      this.rotate = 0;

      // 自动适应容器大小
      this.$nextTick(() => {
        this.adjustImageToContainer();
      });
    },

    // 自动适应容器大小
    adjustImageToContainer() {
      const image = this.$refs.image;
      const wrapper = this.$refs.imageWrapper;

      if (!image || !wrapper) return;

      const imageRatio = image.naturalWidth / image.naturalHeight;
      const containerRatio = wrapper.clientWidth / wrapper.clientHeight;

      // if (imageRatio > containerRatio) {
      //   // 图片更宽，适应宽度
      //   this.scale = wrapper.clientWidth / image.naturalWidth * 1;
      // } else {
      //   // 图片更高，适应高度
      //   this.scale = wrapper.clientHeight / image.naturalHeight * 1;
      // }
    },

    // 放大
    zoomIn() {
      if (this.scale < this.maxScale) {
        this.scale += this.scaleStep;
      }
    },

    // 缩小
    zoomOut() {
      if (this.scale > this.minScale) {
        this.scale -= this.scaleStep;
      }
    },

    // 右转
    rotateRight() {
      this.rotate += 90;
    },

    // 左转
    rotateLeft() {
      this.rotate -= 90;
    },

    // 下载图片
    downloadImage() {
      if (!this.imageUrl) return;

      // 创建一个临时链接
      const link = document.createElement('a');
      link.href = this.imageUrl;
      link.download = `image_${new Date().getTime()}.png`;

      // 触发点击下载
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },

    // 重置查看器状态
    resetViewer() {
      this.imageUrl = '';
      this.scale = 1;
      this.rotate = 0;
    },

    // 关闭对话框
    handleClose() {
      this.resetViewer();
      this.$emit('update:visible', false);
    },
    saveImg() {
      
    },
  }
};
</script>

<style scoped>
.image-viewer-container {
  font-family: 'Helvetica Neue', Arial, sans-serif;
}

.image-viewer-content {
  padding: 10px 0;
}

.image-viewer-toolbar {
  margin-bottom: 15px;
  display: flex;
  gap: 10px;
}

.image-wrapper {
  width: 100%;
  height: 500px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 4px;
  overflow: hidden;
}

.viewable-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  cursor: move;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 500px;
  color: #909399;
}
</style>
