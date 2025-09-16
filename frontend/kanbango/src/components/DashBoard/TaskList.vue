<script setup>
import { ref, nextTick } from 'vue';
import TaskCard from './TaskCard.vue';
import { useBoardStore } from '../../stores/boardStore';
import draggable from 'vuedraggable';
import ConfirmDialog from '../ConfirmDialog.vue';

const props = defineProps({
  list: { type: Object, required: true }
});

const boardStore = useBoardStore();

const isAddingCard = ref(false);
const newCardContent = ref('');
const newCardTextarea = ref(null);

const isEditingTitle = ref(false);
const editedTitle = ref(props.list.title);
const titleInput = ref(null);
const showDeleteConfirm = ref(false);

function showAddCardForm() {
  isAddingCard.value = true;
  nextTick(() => newCardTextarea.value?.focus());
}

async function handleAddCard() {
  if (newCardContent.value.trim() === '') {
    isAddingCard.value = false;
    return;
  }
  await boardStore.createCard(props.list.id, newCardContent.value.trim());
  newCardContent.value = '';
  isAddingCard.value = false;
}

function startEditingTitle() {
  isEditingTitle.value = true;
  editedTitle.value = props.list.title;
  nextTick(() => titleInput.value?.select());
}

async function handleUpdateTitle() {
  if (editedTitle.value.trim() === '' || editedTitle.value.trim() === props.list.title) {
    isEditingTitle.value = false;
    return;
  }
  await boardStore.updateListTitle(props.list.id, editedTitle.value.trim());
  isEditingTitle.value = false;
}

function handleDeleteList() {
  // if (confirm(`确定要删除列表 "${props.list.title}" 吗？`)) {
  //   boardStore.deleteList(props.list.id);
  // }
  showDeleteConfirm.value = true;
}

function onDragEnd() {
    console.log("拖拽结束，最新的看板数据：", boardStore.currentBoard);
}

function onCardDragEnd() {
  boardStore.saveBoardStructure();
}

function confirmDeleteList() {
  // 4. 当用户在模态框中点击“确认”时，这个函数被调用
  boardStore.deleteList(props.list.id);
}
</script>

<template>
  <div class="w-72 bg-gray-100/50 backdrop-blur-sm rounded-lg shadow-md p-3 flex-shrink-0 flex flex-col h-full">
    <div class="flex items-center justify-between mb-4 px-1">
      <h2 v-if="!isEditingTitle" @click="startEditingTitle" class="text-base font-semibold text-gray-700 cursor-pointer w-full">
        {{ list.title }}
      </h2>
      <input 
        v-else
        ref="titleInput"
        v-model="editedTitle"
        @blur="isEditingTitle = false"
        @keyup.enter="handleUpdateTitle"
        @keyup.esc="isEditingTitle = false"
        class="w-full p-1 border-2 border-blue-500 rounded-md focus:outline-none"
      />
      <button @click="handleDeleteList" class="ml-2 text-xl text-gray-500 hover:text-red-500 flex-shrink-0">&times;</button>
    </div>
    
    <div class="overflow-y-auto flex-grow mt-4 flex-wrap">
      <draggable
        v-model="list.cards"
        group="cards"
        item-key="id"
        class="space-y-3 h-full"
        @end="onDragEnd"
      >
        <template #item="{ element: card }">
          <TaskCard
            :card="card"
            :listId="list.id"
          />
        </template>
      </draggable>
    </div>

    <div class="mt-4">
      <div v-if="!isAddingCard">
        <button @click="showAddCardForm" class="w-full text-left px-2 py-1.5 text-sm text-gray-500 hover:bg-gray-300 rounded-md transition-colors">
          + 添加卡片
        </button>
      </div>
      <div v-else>
        <textarea
          ref="newCardTextarea"
          v-model="newCardContent"
          placeholder="输入卡片内容..."
          class="w-full p-2 border-blue-500 border-2 rounded-md focus:outline-none resize-none"
          rows="3"
        ></textarea>
        <div class="mt-2 flex items-center">
          <button @click="handleAddCard" class="px-4 py-2 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700">
            添加卡片
          </button>
          <button @click="isAddingCard = false" class="ml-2 text-2xl text-gray-500 hover:text-gray-800">
            &times;
          </button>
        </div>
      </div>
    </div>
  </div>

  <ConfirmDialog 
    v-model="showDeleteConfirm"
    title="删除列表"
    :message="`确定要删除列表 '${list.title}' 吗？此操作将同时删除其下的所有卡片。`"
    @confirm="confirmDeleteList"
  />
</template>