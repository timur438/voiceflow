<template>
  <button ref="scrollButton" class="scroll-top" @click="scrollToTop">↑</button>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const scrollButton = ref<HTMLButtonElement | null>(null)

const checkScroll = () => {
  if (window.scrollY > 100) {
    scrollButton.value?.classList.add('visible')
  } else {
    scrollButton.value?.classList.remove('visible')
  }
}

onMounted(() => {
  window.addEventListener('scroll', checkScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', checkScroll)
})

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<style scoped>
.scroll-top {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #000;
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  line-height: 50px;
  cursor: pointer;
  opacity: 0;
  visibility: hidden;
  transition:
    opacity 0.3s ease,
    visibility 0.3s ease;
}

.scroll-top.visible {
  opacity: 1;
  visibility: visible;
}
</style>
