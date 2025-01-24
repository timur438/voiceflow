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
        <button v-for="meeting in meetings" :key="meeting.id" class="meeting-item">
          <span>{{ meeting.date }}</span>
          <span>{{ meeting.name }}</span>
          <span>
            <div :class="['status', meeting.status === 'new' ? 'new' : 'old']">{{ meeting.status === 'new' ? 'Новая' : 'Старая' }}</div>
          </span>
          <span>
            <div class="length">{{ meeting.length }}</div>
          </span>
          <span>
            <div class="source">
              <img src="@/assets/img/frame.svg" alt="Frame" class="source-icon" />
              Загружено
            </div>
          </span>
          <img src="@/assets/img/trash.svg" alt="Удалить" class="delete-icon" @click="confirmDelete(meeting)" />
        </button>
      </div>
    </div>
    <div v-if="showPopup" class="popup">
      <div class="popup-content">
        <p class="popup-title">Вы точно хотите удалить встречу?</p>
        <p class="popup-subtext">Встреча "{{ meetingToDelete?.name }}" будет удалена навсегда.<br>Без возможности восстановления.</p>
        <div class="popup-buttons">
          <button class="confirm-button" @click="deleteMeeting">Да</button>
          <button class="cancel-button" @click="cancelDelete">Отменить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import MainSidebar from '@/components/MainSidebar.vue';

interface Meeting {
  id: number;
  date: string;
  name: string;
  status: 'new' | 'old';
  length: string;
}

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

    const meetings = ref<Meeting[]>(Array.from({ length: 30 }, (_, i) => ({
      id: i + 1,
      date: `0${i + 1}.01.2023`,
      name: `Встреча ${i + 1}`,
      status: i % 2 === 0 ? 'new' : 'old',
      length: `${30 + i} мин`
    })));

    const showPopup = ref(false);
    const meetingToDelete = ref<Meeting | null>(null);

    const confirmDelete = (meeting: Meeting) => {
      meetingToDelete.value = meeting;
      showPopup.value = true;
    };

    const deleteMeeting = () => {
      if (meetingToDelete.value) {
        meetings.value = meetings.value.filter(meeting => meeting.id !== meetingToDelete.value!.id);
        showPopup.value = false;
      }
    };

    const cancelDelete = () => {
      showPopup.value = false;
    };

    return { goToHome, meetings, showPopup, meetingToDelete, confirmDelete, deleteMeeting, cancelDelete };
  }
});
</script>

<style scoped src="@/assets/scss/MainView.scss"></style>
