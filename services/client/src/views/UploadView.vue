<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const file = ref(null)
const message = ref('')
const uploading = ref(false)
const previewUrl = ref(null)

const handleFileChange = (event) => {
    file.value = event.target.files[0]
    if (file.value) {
        previewUrl.value = URL.createObjectURL(file.value)
    }
}

const uploadPhoto = async () => {
    if (!file.value) return

    uploading.value = true
    message.value = ''
    
    const formData = new FormData()
    formData.append('file', file.value)

    try {
        await axios.post(`http://localhost:5001/upload/${route.params.slug}`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        message.value = 'Upload successful!'
        file.value = null
        previewUrl.value = null
    } catch (error) {
        console.error(error)
        message.value = 'Upload failed.'
    } finally {
        uploading.value = false
    }
}
</script>

<template>
    <div class="min-h-screen bg-gray-900 flex flex-col justify-center items-center px-4">
        <h1 class="text-white text-3xl font-bold mb-8">Upload Photo</h1>
        
        <div class="w-full max-w-sm bg-white rounded-lg shadow-xl overflow-hidden p-6">
            <div v-if="previewUrl" class="mb-4">
                <img :src="previewUrl" class="w-full h-48 object-cover rounded-md" />
            </div>

            <div class="flex items-center justify-center w-full">
                <label for="dropzone-file" class="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100">
                    <div class="flex flex-col items-center justify-center pt-5 pb-6">
                        <svg class="w-10 h-10 mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                        <p class="mb-2 text-sm text-gray-500"><span class="font-semibold">Click to upload</span></p>
                        <p class="text-xs text-gray-500">PNG, JPG or GIF</p>
                    </div>
                    <input id="dropzone-file" type="file" class="hidden" @change="handleFileChange" accept="image/*" />
                </label>
            </div> 

            <button @click="uploadPhoto" :disabled="!file || uploading" class="w-full mt-4 bg-indigo-600 text-white font-bold py-2 px-4 rounded hover:bg-indigo-700 disabled:opacity-50">
                <span v-if="uploading">Uploading...</span>
                <span v-else>Send Photo</span>
            </button>
            
            <p v-if="message" class="mt-4 text-center" :class="message.includes('success') ? 'text-green-600' : 'text-red-600'">{{ message }}</p>
        </div>
    </div>
</template>
