<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center items-center">
    <h1 class="text-4xl font-bold text-indigo-600 mb-4">PictureBoard</h1>
    <p class="text-lg text-gray-600 mb-8">Share memories in real-time.</p>
    <div class="space-x-4">
      <router-link to="/login" class="px-6 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700">Login</router-link>
      <router-link to="/register" class="px-6 py-2 bg-white text-indigo-600 border border-indigo-600 rounded hover:bg-gray-50">Register</router-link>
    </div>
  </div>
</template>
