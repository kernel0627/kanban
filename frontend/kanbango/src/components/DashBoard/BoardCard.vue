<script setup>
import { ref, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { useBoardStore } from '../../stores/boardStore';
// import vuedraggable from 'vuedraggable';
import ConfirmDialog from '../ConfirmDialog.vue';

const props = defineProps({
  board: { type: Object, required: true }
});

const boardStore = useBoardStore();
const router = useRouter();
const isEditing = ref(false);
const titleInput = ref(null);
const editedTitle = ref(props.board.title);
const showDeleteConfirm = ref(false);


function startEditing() {
    isEditing.value = true;
    editedTitle.value = props.board.title;
    nextTick(() => {
        titleInput.value?.focus();
    });
}

async function handleUpdateBoardTitle() {
  if (editedTitle.value.trim() === '' || editedTitle.value.trim() === props.board.title) {
    isEditing.value = false;
    return;
  }
  await boardStore.updateBoardTitle(props.board.id, editedTitle.value.trim());
  isEditing.value = false;
}

async function handleDeleteBoard() {
  // if (confirm(`确定要删除看板 "${props.board.title}" 吗？`)) {
  //   await boardStore.deleteBoard(props.board.id);
  // }
  showDeleteConfirm.value = true;
}

function navigateToBoard() {
  if (!isEditing.value) {
    router.push({ name: 'board', params: { id: props.board.id } });
  }
}
function confirmDeleteBoard() {
  boardStore.deleteBoard(props.board.id);
}
</script>

<template>
  <div 
    @click="navigateToBoard"
    class="bg-white rounded-lg shadow p-4 group relative flex items-center justify-between cursor-pointer hover:shadow-lg transition-shadow"
  >
    <div v-if="!isEditing" class="w-full">
      <h2 class="font-bold text-lg text-gray-800">{{ board.title }}</h2>
    </div>
    <div v-else class="w-full">
      <input 
        ref="titleInput"
        type="text"
        v-model="editedTitle"
        @click.stop @keyup.enter.prevent="handleUpdateBoardTitle"
        @blur="handleUpdateBoardTitle"
        @keyup.esc="isEditing = false"
        class="w-full p-1 border-2 border-blue-500 rounded focus:outline-none"
      />
    </div>

    <div class="flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-opacity ml-4">
        <button @click.stop="startEditing" class="w-6 h-6 text-sm text-gray-500 hover:text-blue-600 flex items-center justify-center rounded hover:bg-gray-200" title="编辑">✏️</button>
        <button @click.stop="handleDeleteBoard" class="w-6 h-6 text-sm text-gray-500 hover:text-red-500 flex items-center justify-center rounded hover:bg-gray-200" title="删除">🗑️</button>
    </div>
  </div>

  <ConfirmDialog 
    v-model="showDeleteConfirm"
    title="删除看板"
    :message="`确定要删除看板 '${board.title}' 吗？此操作将同时删除其下的所有列表。`"
    @confirm="confirmDeleteBoard"
  />
</template>