<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const message = ref('Loading...')
const user = ref(null)
const boards = ref([])
const showCreateModal = ref(false)
const newBoardTitle = ref('')
const newBoardSlug = ref('')
const createError = ref('')
const router = useRouter()

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

const getStatus = async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/login')
    return
  }
  try {
    const res = await axios.get('http://localhost:5001/auth/status', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    user.value = res.data.data
    message.value = `Welcome, ${user.value.email}!`
    getBoards()
  } catch (error) {
    console.error(error)
    logout()
  }
}

const getBoards = async () => {
  const token = localStorage.getItem('token')
  try {
    const res = await axios.get('http://localhost:5001/boards', {
       headers: { 'Authorization': `Bearer ${token}` }
    })
    boards.value = res.data.data
  } catch (error) {
    console.error(error)
  }
}

const createBoard = async () => {
  const token = localStorage.getItem('token')
  try {
    await axios.post('http://localhost:5001/boards', {
      title: newBoardTitle.value,
      slug: newBoardSlug.value
    }, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    showCreateModal.value = false
    newBoardTitle.value = ''
    newBoardSlug.value = ''
    getBoards()
  } catch (error) {
    createError.value = error.response?.data?.message || 'Error creating board'
  }
}

onMounted(() => {
  getStatus()
})
</script>

<template>
  <div class="min-h-screen bg-gray-100">
    <nav class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <h1 class="text-xl font-bold text-indigo-600">PictureBoard</h1>
            </div>
          </div>
          <div class="flex items-center">
             <span v-if="user" class="mr-4 text-gray-700">{{ user.email }}</span>
            <button @click="logout" class="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700">Logout</button>
          </div>
        </div>
      </div>
    </nav>
    
    <div class="py-10">
      <header>
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 class="text-3xl font-bold leading-tight text-gray-900">Dashboard</h1>
          <button @click="showCreateModal = true" class="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700">
            + New Board
          </button>
        </div>
      </header>
      <main>
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8 mt-6">
          
          <div v-if="boards.length === 0" class="text-center py-12">
            <p class="text-gray-500 text-lg">You haven't created any boards yet.</p>
          </div>

          <div v-else class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
             <div v-for="board in boards" :key="board.id" class="bg-white overflow-hidden shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                   <h3 class="text-lg leading-6 font-medium text-gray-900">{{ board.title }}</h3>
                   <p class="mt-1 text-sm text-gray-500">/{{ board.slug }}</p>
                   <div class="mt-4">
                      <router-link :to="`/board/${board.id}/settings`" class="text-indigo-600 hover:text-indigo-900">Settings</router-link>
                   </div>
                </div>
             </div>
          </div>

        </div>
      </main>
    </div>

    <!-- Create Modal -->
    <div v-if="showCreateModal" class="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true" @click="showCreateModal = false"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">Create New Board</h3>
                <div class="mt-4 space-y-4">
                   <input v-model="newBoardTitle" type="text" placeholder="Event Title (e.g. Smith Wedding)" class="w-full border border-gray-300 rounded px-3 py-2" />
                   <input v-model="newBoardSlug" type="text" placeholder="URL Slug (e.g. smith-wedding)" class="w-full border border-gray-300 rounded px-3 py-2" />
                   <p v-if="createError" class="text-red-500 text-sm">{{ createError }}</p>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button @click="createBoard" type="button" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none sm:ml-3 sm:w-auto sm:text-sm">
              Create
            </button>
            <button @click="showCreateModal = false" type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>