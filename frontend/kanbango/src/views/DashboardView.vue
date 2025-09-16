<!-- DashboardView.vue -->
<!-- <template>
    <div class="p-8">
        <div class="flex justify-between items-center mb-8">
            <h1 class="text-3xl font-bold text-gray-800">My KanbanGO</h1>
            <RouterLink
                to="/boards/new"
                class="px-4 py-2 bg-blue-600 text-white rounded shadow-sm hover:bg-blue-700">
                Add Board
            </RouterLink>
        </div>

        <div v-if="boardStore.isLoading">Loading……</div>
        <div v-else-if="boardStore.boards.length === 0" class="text-center text-gray-500 mt-16">
            <p>No boards available</p>
            <p>
                Click the button at the right corner to create your first board!
            </p>
        </div>
        <div 
            v-else
            class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6"
        >
            <RouterLink 
                v-for="board in boardStore.boards"
                :key="board.id"
                :to="{name:'board' , params:{id:board.id}}"
                class="bg-white rounded-lg shadow p-4 cursor-pointer hover:shadow-lg transition-shadow"
                >
                <h2 class="text-lg font-bold text-gray-800 mb-2">{{ board.title }}</h2>
            </RouterLink>

        </div>

    </div>
</template> -->

<template>
    <div class="p-8">
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800">我的看板</h1>
        <RouterLink to="/boards/new" class="px-4 py-2 bg-blue-600 text-white font-semibold rounded-md shadow-sm hover:bg-blue-700 cursor-pointer">
          + 创建新看板
        </RouterLink>
      </div>
  
      <div v-if="boardStore.isLoading">正在加载看板...</div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 flex-grow">
        <BoardCard
          class="hover:shadow-lg transition-shadow cursor-pointer"
          v-for="board in boardStore.boards"
          :key="board.id"
          :board="board"
        />
        
        <RouterLink to="/boards/new" class="bg-gray-200 rounded-lg shadow p-4 flex items-center justify-center text-gray-500 hover:cursor-pointer hover:bg-gray-300">
          <span>+ 添加看板</span>
        </RouterLink>
      </div>
    </div>
  </template>

<script setup>
import {onMounted} from 'vue';
import {useBoardStore} from '../stores/boardStore';
import {RouterLink} from 'vue-router';
import BoardCard from '../components/DashBoard/BoardCard.vue';

const boardStore = useBoardStore();

onMounted(() => {
    boardStore.fetchBoards();
})

</script>