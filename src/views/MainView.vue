<template>
  <div class="main-container">
    <MainSidebar />
    <div class="content">
      <div class="header">
        <h1>Мои встречи</h1>
        <button class="add-meeting-button">
          Добавить встречу
          <img src="@/assets/img/add.svg" alt="Добавить" class="add-icon" />
        </button>
        <div class="account-info">
          <div class="account-circle"></div>
          <span class="account-email">example@example.com</span>
        </div>
      </div>
      <div class="meeting-header">
        <span>Дата</span>
        <span>Название</span>
        <span>Статус</span>
        <span>Длина</span>
        <span>Источник</span>
      </div>
      <div class="meeting-list">
        <div class="meeting-item">
          <span>01.01.2023</span>
          <span>Встреча с клиентом</span>
          <span>
            <div class="status new">Новая</div>
          </span>
          <span>30 мин</span>
          <span>Загружено</span>
        </div>
        <div class="meeting-item">
          <span>02.01.2023</span>
          <span>Обсуждение проекта</span>
          <span>
            <div class="status old">Старая</div>
          </span>
          <span>1 час</span>
          <span>Загружено</span>
        </div>
        <!-- Add more meeting items here -->
      </div>
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
