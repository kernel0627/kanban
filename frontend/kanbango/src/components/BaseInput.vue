<template>
    <input 
        v-model="model"
        class = 'w-full px-4 py-2 border-gray-300 rounded-md focusLoutline-none focus:ring-blue-500'
        >
</template>

<script setup>
    const model = defineModel()
</script>
