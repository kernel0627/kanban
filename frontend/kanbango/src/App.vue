<template>
    <div class="min-h-screen ">
        <Navbar  />

        <main>
            <RouterView />
        </main>
    </div>        
    

</template>

<script setup>
import { RouterView } from 'vue-router';
import { useUserStore } from './stores/userStore';
import Navbar from './components/Navbar.vue';

const userStore = useUserStore()
</script>

<style>

</style>