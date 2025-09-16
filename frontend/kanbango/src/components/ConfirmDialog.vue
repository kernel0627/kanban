<script setup>
const props = defineProps({
  modelValue: { type: Boolean, required: true }, // 使用 v-model 控制显示/隐藏
  title: { type: String, default: '确认操作' },
  message: { type: String, default: '你确定要执行此操作吗？' }
});

const emit = defineEmits(['update:modelValue', 'confirm']);

function confirmAction() {
  emit('confirm');
  closeDialog();
}

function closeDialog() {
  emit('update:modelValue', false);
}
</script>

<template>
  <Transition name="fade">
    <div 
      v-if="modelValue" 
      @click.self="closeDialog" 
      class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center"
    >
      <div class="bg-white rounded-lg shadow-xl p-6 w-full max-w-sm">
        <h3 class="text-lg font-bold text-gray-800">{{ title }}</h3>
        <p class="mt-2 text-sm text-gray-600">{{ message }}</p>
        <div class="mt-6 flex justify-end space-x-4">
          <button @click="closeDialog" class="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300">
            取消
          </button>
          <button @click="confirmAction" class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700">
            确认
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>