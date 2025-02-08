<template>
  <div class="main-container">
    <MainSidebar @navigateToMain="goToHome" />
    <div class="content">
      <div class="header" @click="goToHome">
        <h1>{{ $t('myMeetings') }}</h1>
        <button class="add-meeting-button" @click.stop="showUploadPopup = true">
          {{ $t('addMeeting') }}
          <img src="@/assets/img/add.svg" alt="Add" class="add-icon" />
        </button>
        <div class="account-info" @click="goToSettings" style="cursor: pointer;">
          <div class="account-circle"></div>
          <span class="account-email">example@example.com</span>
        </div>
      </div>
      <div class="meeting-header">
        <span>{{ $t('date') }}</span>
        <span>{{ $t('name') }}</span>
        <span>{{ $t('status') }}</span>
        <span>{{ $t('length') }}</span>
        <span>{{ $t('source') }}</span>
      </div>
      <div class="meeting-list">
        <button v-for="meeting in meetings" :key="meeting.id" class="meeting-item" @click="goToMeeting(meeting.id)">
          <span>{{ meeting.date }}</span>
          <span>{{ meeting.name }}</span>
          <span>
            <div :class="['status', meeting.status === 'new' ? 'new' : 'old']">{{ meeting.status === 'new' ? $t('new') : $t('old') }}</div>
          </span>
          <span>
            <div class="length">{{ meeting.length }}</div>
          </span>
          <span>
            <div class="source">
              <img src="@/assets/img/frame.svg" alt="Frame" class="source-icon" />
              {{ $t('uploaded') }}
            </div>
          </span>
          <img src="@/assets/img/trash.svg" alt="Delete" class="delete-icon" @click.stop="confirmDelete(meeting)" />
        </button>
      </div>
    </div>
    <div v-if="showPopup" class="popup">
      <div class="popup-content">
        <p class="popup-title">{{ $t('confirmDelete') }}</p>
        <p class="popup-subtext">{{ $t('deleteForever', { meetingName: meetingToDelete?.name }) }}</p>
        <div class="popup-buttons">
          <button class="confirm-button" @click="deleteMeeting">{{ $t('yes') }}</button>
          <button class="cancel-button" @click="cancelDelete">{{ $t('cancel') }}</button>
        </div>
      </div>
    </div>
    <div v-if="showUploadPopup" class="popup">
      <div class="popup-content upload-popup">
        <div class="popup-header">
          <span>{{ $t('uploadFile') }}</span>
          <button class="close-button" @click="showUploadPopup = false">×</button>
        </div>
        <div class="upload-body">
          <div class="drop-area" @click="openFileDialog">
            <p><span>{{ $t('chooseFile') }}</span> {{ $t('orDrag') }}</p>
            <p class="drop-describe">{{ $t('anyFile') }}</p>
            <input type="file" ref="fileInput" style="display: none;" @change="handleFileChange" />
          </div>
          <div class="meeting-name">
            <label for="meeting-name">{{ $t('meetingName') }}</label>
            <input type="text" id="meeting-name" v-model="meetingName" :placeholder="$t('meetingNamePlaceholder')" />
          </div>
        </div>
        <div class="popup-footer">
          <button class="upload-button">{{ $t('uploadMeeting') }}</button>
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

    const goToSettings = (event: Event) => {
      event.stopPropagation();
      router.push({ name: 'SettingsView' });
    };

    const goToMeeting = (id: number) => {
      router.push({ name: 'MeetingView', params: { id } });
    };

    const meetings = ref<Meeting[]>(Array.from({ length: 30 }, (_, i) => ({
      id: i + 1,
      date: `0${i + 1}.01.2023`,
      name: `Встреча ${i + 1}`,
      status: i % 2 === 0 ? 'new' : 'old',
      length: `${30 + i} мин`
    })));

    const showPopup = ref(false);
    const showUploadPopup = ref(false);
    const meetingToDelete = ref<Meeting | null>(null);
    const meetingName = ref('');
    const fileInput = ref<HTMLInputElement | null>(null);

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

    const openFileDialog = () => {
      fileInput.value?.click();
    };

    const handleFileChange = (event: Event) => {
      const input = event.target as HTMLInputElement;
      if (input.files && input.files[0]) {
        const file = input.files[0];
        uploadFile(file);
      }
    };

    const uploadFile = async (file: File) => {
      const formData = new FormData();
      formData.append('file', file);

      const requestData = {
        group_segments: true,
        transcript_output_format: 'both',
        num_speakers: 2,
        translate: false,
        language: 'en',
        prompt: '',
        summary_type: 'summary',
        offset_seconds: 0
      };

      formData.append('request', JSON.stringify(requestData));

      try {
        const response = await fetch('https://voiceflow.ru/api/transcribe', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          const errorResponse = await response.json();
          console.error('Ошибка при отправке файла на сервер:', errorResponse);
          throw new Error('Ошибка при отправке файла на сервер');
        }

        const result = await response.json();
        console.log('Результат транскрипции:', result);
      } catch (error) {
        console.error('Ошибка:', error);
      }
    };

    return { goToHome, goToSettings, goToMeeting, meetings, showPopup, showUploadPopup, meetingToDelete, meetingName, fileInput, confirmDelete, deleteMeeting, cancelDelete, openFileDialog, handleFileChange, uploadFile };
  }
});
</script>

<style scoped src="@/assets/scss/MainView.scss"></style>
