<!-- TaskCard.vue -->
<template> 
    <div class="bg-white p-3 rounded-md shadow-sm border-b border-gray-200 group relative flex items-center justify-between">
        <div v-if="!isEditing" @click="startEditing" class="cursor-pointer">
            <p class="text-sm text-gray-800 whitespace-pre-wrap">{{ card.content }}</p>
        </div>
        <div v-else >
            <textarea 
            ref="cardTextarea"
            v-model="editedContent"
            @blur="handleUpdateCard"
            @keyup.enter.prevent="handleUpdateCard"
            @keyup.esc="cancelEditing"
            class="w-full p-2 border-blue-500 border-2 rounded-md focus:outline-none resize-none"
            rows="3">
            </textarea>
            <button @click="handleUpdateCard" class="px-3 py-1 mt-2 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700">Save</button>
            <button @click="cancelEditing" class="px-3 py-1 mt-2 bg-gray-300 text-gray-800 text-sm rounded-md hover:bg-gray-400">Cancel</button>
        </div>

        <div class="flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-opacity ml-4">
            <button @click="startEditing" class="w-6 h-6 text-sm text-gray-500 hover:text-blue-600 flex items-center justify-center rounded hover:bg-gray-200" title="编辑">✏️</button>
            <button @click="handleDeleteCard" class="w-6 h-6 text-sm text-gray-500 hover:text-red-500 flex items-center justify-center rounded hover:bg-gray-200">🗑️</button>
        </div>

        
        
    </div>
    <ConfirmDialog 
        v-model="confirmDelete"
        title="删除卡片"
        :message="`确定要删除卡片 '${card.content}' 吗？`"
        @confirm="confirmDeleteCard"
    />

</template>

<script setup>
import {ref , nextTick} from 'vue';
import { useBoardStore } from '../../stores/boardStore';
import ConfirmDialog from '../ConfirmDialog.vue';

const boardStore = useBoardStore();

const props = defineProps({
    listId:{type:Number,required:true},
    card:{type:Object,required:true}
})

// const emit = defineEmits(['update-card','delete-card'])

const isEditing = ref(false)
const editedContent = ref(props.card.content)
const cardTextarea = ref(null)
const confirmDelete = ref(false)

function startEditing(){
    isEditing.value = true 
    editedContent.value = props.card.content 
    nextTick(() => {
        cardTextarea.value?.focus()
    })
}

function cancelEditing() {
  isEditing.value = false;
  editedContent.value = props.card.content; 
}

async function handleUpdateCard(){
    if (editedContent.value.trim() === '' || editedContent.value.trim() === props.card.content){
        isEditing.value = false;
        return;
    }
    // emit('update-card', {
    //     cardId: props.card.id , 
    //     newContent: editedContent.value.trim()
    // })

    await boardStore.updateCardContent( props.card.id, editedContent.value.trim());
    isEditing.value = false;
}

function handleDeleteCard(){
    // if (confirm('Are you sure you want to delete this card?')){
    //     // emit('delete-card', props.card.id)
    //     await boardStore.deleteCard(props.listId, props.card.id);
    // }
    confirmDelete.value = true;

}

function confirmDeleteCard(){
    boardStore.deleteCard(props.listId, props.card.id);
}

    

</script>
