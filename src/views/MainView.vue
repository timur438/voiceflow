<template>
  <div class="main-container">
    <aside class="sidebar">
      <div class="sidebar-content">
        <div class="logo">
          <div class="logo-box"></div>
          <button class="logo-button" @click="goToHome">Whisper</button>
        </div>
        <nav class="menu">
          <ul>
            <li><a href="#"><img src="@/assets/img/category.svg" alt="Мои встречи" />Мои встречи</a></li>
            <li><a href="#"><img src="@/assets/img/setting.svg" alt="Настройки и интеграции" />Настройки и интеграции</a></li>
            <li><a href="#"><img src="@/assets/img/logout.svg" alt="Выйти" />Выйти</a></li>
          </ul>
        </nav>
      </div>
    </aside>
    <div class="content">
      <h1>Добро пожаловать на главную страницу</h1>
      <!-- Add more content here -->
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'MainView',
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
