<template>
  <div class="main-container">
    <MainSidebar />
    <div class="content">
      <h1>Добро пожаловать на главную страницу</h1>
      <!-- Add more content here -->
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';
import MainSidebar from '@/components/MainSidebar.vue';

export default defineComponent({
  name: 'MainView',
  components: {
    MainSidebar
  },
  setup() {
    const router = useRouter();
    const goToHome = () => {
      router.push({ name: 'MainView' });
    };
    return { goToHome };
  }
});
</script>

<style scoped src="@/assets/scss/MainView.scss"></style>
