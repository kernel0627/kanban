<script setup>
import { onMounted, computed, ref, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import { useBoardStore } from '../stores/boardStore';
import TaskList from '../components/DashBoard/TaskList.vue';
import draggable from 'vuedraggable';

const route = useRoute();
const boardStore = useBoardStore();
const boardId = computed(() => parseInt(route.params.id));

const isAddingList = ref(false);
const newListTitle = ref('');
const newListInput = ref(null);

onMounted(() => {
    boardStore.fetchBoard(boardId.value);
});

function showAddListForm() {
    isAddingList.value = true;
    nextTick(() => newListInput.value?.focus());
}

async function handleAddList() {
    if (newListTitle.value.trim() === '') {
        isAddingList.value = false;
        return;
    }
    await boardStore.createList(boardId.value, newListTitle.value.trim());
    newListTitle.value = '';
}

function onListDragEnd() {
    boardStore.saveBoardStructure();
}
</script>

<template>
    <div v-if="boardStore.isLoading || !boardStore.currentBoard" class="p-8 text-center">Loading...</div>
    <div v-else class="p-8 h-screen flex flex-col">
        <h1 class="text-4xl font-bold text-gray-700 tracking-tight mb-8 text-center font-poppins">
            {{ boardStore.currentBoard.title }}
        </h1>

        <div class="flex-grow overflow-y-auto">
            <draggable
                v-model="boardStore.currentBoard.lists"
                item-key="id"
                class="flex justify-center flex-wrap gap-6"
                @end="onListDragEnd"
            >
                <template #item="{ element: list }">
                    <TaskList :list="list" />
                </template>

                <template #footer>
                    <div class="w-72 flex-shrink-0">
                        <div v-if="!isAddingList">
                            <button @click="showAddListForm" class="w-full p-3 flex items-center justify-center font-semibold text-gray-500 bg-white/50 rounded-lg border-2 border-dashed border-gray-400 hover:bg-blue-500 hover:text-white hover:border-solid hover:border-blue-500 transition-all duration-300">
                                + 添加列表
                            </button>
                        </div>
                        <div v-else class="bg-gray-100 rounded-lg p-3">
                            <input 
                                ref="newListInput"
                                v-model="newListTitle"
                                @keyup.enter="handleAddList"
                                @keyup.esc="isAddingList = false"
                                placeholder="输入列表标题..."
                                class="w-full p-2 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                                type="text">
                            <div class="mt-2 flex items-center">
                                <button @click="handleAddList" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">添加列表</button>
                                <button @click="isAddingList = false" class="ml-2 text-2xl text-gray-500 hover:text-gray-700">&times;</button>
                            </div>
                        </div>
                    </div>
                </template>
            </draggable>
        </div>
    </div>
</template>