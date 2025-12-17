<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'
import { io } from 'socket.io-client'

const route = useRoute()
const board = ref(null)
const photos = ref([])
const loading = ref(true)
const socket = ref(null)
const scrollContainer = ref(null)

const fetchBoardData = async () => {
    try {
        const res = await axios.get(`http://localhost:5001/view/${route.params.slug}`)
        board.value = res.data.data.board
        photos.value = res.data.data.photos
        loading.value = false
    } catch (error) {
        console.error(error)
        loading.value = false
    }
}

const setupSocket = () => {
    socket.value = io('http://localhost:5001')
    
    socket.value.on('connect', () => {
        console.log('Connected to socket server')
        socket.value.emit('join', { room: route.params.slug })
    })

    socket.value.on('new_photo', (photo) => {
        console.log('New photo received:', photo)
        photos.value.push(photo)
        nextTick(() => {
            scrollToBottom()
        })
    })
}

const scrollToBottom = () => {
    if (scrollContainer.value) {
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
    }
}

// Simple auto-scroll logic (Proof of Concept)
let autoScrollInterval;
const startAutoScroll = () => {
    // Only auto-scroll if we are in "masonry" mode for example
    // For now, just a simple slow scroll
    autoScrollInterval = setInterval(() => {
        window.scrollBy(0, 1)
    }, 50)
}

onMounted(async () => {
    await fetchBoardData()
    if (board.value) {
        setupSocket()
        startAutoScroll()
    }
})

onUnmounted(() => {
    if (socket.value) socket.value.disconnect()
    if (autoScrollInterval) clearInterval(autoScrollInterval)
})
</script>

<template>
    <div class="min-h-screen bg-black text-white">
        <div v-if="loading" class="flex justify-center items-center h-screen">
            <p>Loading Board...</p>
        </div>
        
        <div v-else ref="scrollContainer" class="p-4">
             <!-- Header (Optional, maybe fade out) -->
             <div class="fixed top-0 left-0 w-full bg-black bg-opacity-50 p-4 z-10 flex justify-between items-center">
                 <h1 class="text-2xl font-bold">{{ board.title }}</h1>
                 <div class="text-sm">Scan to Upload: app.com/upload/{{ board.slug }}</div>
             </div>

             <!-- Masonry Grid (Simple Implementation using columns) -->
             <div class="columns-1 md:columns-2 lg:columns-3 xl:columns-4 gap-4 mt-16 space-y-4">
                 <div v-for="photo in photos" :key="photo.id" class="break-inside-avoid">
                     <img :src="photo.url" class="w-full rounded-lg shadow-lg" loading="lazy" />
                 </div>
             </div>
             
             <!-- Empty State -->
             <div v-if="photos.length === 0" class="flex justify-center items-center h-64 mt-20">
                 <p class="text-gray-500 text-xl">Waiting for photos...</p>
             </div>
        </div>
    </div>
</template>

<style scoped>
/* Tailwind 'columns' utility provides a decent masonry layout without JS */
</style>
