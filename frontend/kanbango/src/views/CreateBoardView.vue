<!-- CreateBoardView.vue -->
<template>
    <div class="flex items-center justify-center min-h-screen bg-gray-200">
        <div class="w-full max-w-md p-6 space-y-6 bg-white rounded-xl shadow-lg">
            <h1 class="text-3xl font-bold text-center text-gray-800">Create New Board</h1>
            <form @submit.prevent="handleCreateBoard" class = 'space-y-6'>
                <div>
                    <label for="board-title" class="block">
                        Board Title
                    </label>
                    <BaseInput 
                    id="board-title"
                    type="text"
                    v-model="newBoardTitle" 
                    placeholder="Enter board title" 
                    class="mt-1"
                    />
                </div>
                <BaseButton type="submit" :disabled="isLoading" class="w-full">
                    {{ isLoading ? 'Creating...' : 'Create Board' }}
                </BaseButton>
            </form>
        </div>
    </div>
</template>

<script setup>
import {ref} from 'vue';
import {useRouter} from 'vue-router'
import { useBoardStore } from '../stores/boardStore';
import BaseInput from '../components/BaseInput.vue';
import BaseButton from '../components/BaseButton.vue';

const boardStore = useBoardStore();
const router = useRouter();
const newBoardTitle = ref('');
const isLoading = ref(false);

async function handleCreateBoard(){
    if (newBoardTitle.value.trim() === ''){
        alert('Board title cannot be empty');
        return;
    }
    isLoading.value = true;
    try{
        const newBoard = await boardStore.createBoard(newBoardTitle.value)
        console.log(newBoard)
        router.push({name:'board' , params:{id:newBoard.id}})
    }catch(err){
        alert('Failed to create board. Please try again.')
    }finally{
        isLoading.value = false;
    }
}


</script>

