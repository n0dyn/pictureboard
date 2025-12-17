<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import QrcodeVue from 'qrcode.vue'

const route = useRoute()
const router = useRouter()
const board = ref(null)
const loading = ref(true)
const message = ref('')

// Form fields
const title = ref('')
const animationMode = ref('masonry')
const scrollSpeed = ref(10)

const uploadUrl = computed(() => {
    if (!board.value) return ''
    // In production, this would be the actual domain
    return `${window.location.origin}/upload/${board.value.slug}`
})

const viewUrl = computed(() => {
    if (!board.value) return ''
    return `${window.location.origin}/view/${board.value.slug}`
})

const fetchBoard = async () => {
    const token = localStorage.getItem('token')
    try {
        const res = await axios.get(`http://localhost:5001/boards/${route.params.id}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        board.value = res.data.data
        title.value = board.value.title
        animationMode.value = board.value.settings.animation_mode
        scrollSpeed.value = board.value.settings.scroll_speed
    } catch (error) {
        console.error(error)
        router.push('/dashboard')
    } finally {
        loading.value = false
    }
}

const saveSettings = async () => {
    const token = localStorage.getItem('token')
    try {
        await axios.put(`http://localhost:5001/boards/${route.params.id}`, {
            title: title.value,
            settings: {
                animation_mode: animationMode.value,
                scroll_speed: parseInt(scrollSpeed.value)
            }
        }, {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        message.value = 'Settings saved successfully!'
        setTimeout(() => message.value = '', 3000)
    } catch (error) {
        console.error(error)
        message.value = 'Error saving settings.'
    }
}

onMounted(() => {
    fetchBoard()
})
</script>

<template>
    <div class="min-h-screen bg-gray-100">
        <nav class="bg-white shadow">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex justify-between h-16">
                    <div class="flex items-center">
                        <router-link to="/dashboard" class="text-indigo-600 font-bold text-xl">PictureBoard</router-link>
                        <span class="mx-2 text-gray-400">/</span>
                        <span class="text-gray-500">Settings</span>
                    </div>
                </div>
            </div>
        </nav>

        <main class="max-w-7xl mx-auto py-10 px-4 sm:px-6 lg:px-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- Settings Form -->
            <div class="lg:col-span-2">
                <div v-if="loading" class="text-center">Loading...</div>
                <div v-else class="bg-white shadow rounded-lg p-6">
                    <h2 class="text-2xl font-bold text-gray-900 mb-6">Board Settings: {{ board.title }}</h2>
                    
                    <form @submit.prevent="saveSettings" class="space-y-6">
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Board Title</label>
                            <input v-model="title" type="text" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                        </div>

                        <div>
                             <label class="block text-sm font-medium text-gray-700">Animation Mode</label>
                             <select v-model="animationMode" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md">
                                 <option value="masonry">Masonry (Infinite Wall)</option>
                                 <option value="slideshow">Ken Burns Slideshow</option>
                                 <option value="carousel">Ticker/Carousel</option>
                             </select>
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-gray-700">Scroll/Transition Speed (seconds)</label>
                            <input v-model="scrollSpeed" type="number" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                        </div>

                        <div class="flex justify-between items-center">
                            <button type="submit" class="bg-indigo-600 border border-transparent rounded-md shadow-sm py-2 px-4 inline-flex justify-center text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                                Save Changes
                            </button>
                            <span v-if="message" class="text-green-600 font-medium">{{ message }}</span>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Links & QR Code -->
            <div class="lg:col-span-1 space-y-6">
                 <div class="bg-white shadow rounded-lg p-6">
                    <h3 class="text-lg font-medium text-gray-900 mb-4">Guest Upload Link</h3>
                    <div class="flex flex-col items-center">
                        <qrcode-vue v-if="uploadUrl" :value="uploadUrl" :size="200" level="H" />
                        <a :href="uploadUrl" target="_blank" class="mt-4 text-indigo-600 hover:text-indigo-900 break-all text-center">{{ uploadUrl }}</a>
                        <p class="text-sm text-gray-500 mt-2 text-center">Scan this code to upload photos.</p>
                    </div>
                </div>

                <div class="bg-white shadow rounded-lg p-6">
                    <h3 class="text-lg font-medium text-gray-900 mb-4">Display Link</h3>
                    <div class="flex flex-col items-center">
                        <a :href="viewUrl" target="_blank" class="text-indigo-600 hover:text-indigo-900 break-all text-center text-lg font-bold">Open Board Viewer</a>
                        <p class="text-sm text-gray-500 mt-2 text-center">Open this on the big screen.</p>
                    </div>
                </div>
            </div>

        </main>
    </div>
</template>

