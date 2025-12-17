<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const login = async () => {
  try {
    const res = await axios.post('http://localhost:5001/auth/login', {
      email: email.value,
      password: password.value
    })
    localStorage.setItem('token', res.data.auth_token)
    router.push('/dashboard')
  } catch (err) {
    error.value = err.response?.data?.message || 'Login failed'
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="max-w-md w-full space-y-8 p-8 bg-white shadow rounded">
      <h2 class="text-center text-3xl font-extrabold text-gray-900">Sign in to your account</h2>
      <form class="mt-8 space-y-6" @submit.prevent="login">
        <input type="email" v-model="email" required placeholder="Email address" class="appearance-none rounded relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
        <input type="password" v-model="password" required placeholder="Password" class="appearance-none rounded relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm mt-4" />
        <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>
        <button type="submit" class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
          Sign in
        </button>
      </form>
       <div class="text-center">
         <router-link to="/register" class="text-indigo-600 hover:text-indigo-500">Need an account? Register</router-link>
      </div>
    </div>
  </div>
</template>
