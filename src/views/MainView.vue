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

    <!-- Delete Confirmation Popup -->
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

    <!-- Upload Popup -->
    <div v-if="showUploadPopup" class="popup">
      <div class="popup-content upload-popup">
        <div class="popup-header">
          <span>{{ $t('uploadFile') }}</span>
          <button class="close-button" @click="closeUploadPopup">×</button>
        </div>
        <div class="upload-body">
          <div class="drop-area" 
               @click="openFileDialog"
               @drop="handleDrop"
               @dragover="handleDragOver">
            <template v-if="!isFileSelected">
              <p><span>{{ $t('chooseFile') }}</span> {{ $t('orDrag') }}</p>
              <p class="drop-describe">{{ $t('anyFile') }}</p>
            </template>
            <template v-else>
              <div class="selected-file">
                <img src="@/assets/img/folder.svg" alt="Folder" class="folder-icon" />
                <span>{{ selectedFile?.name }}</span>
              </div>
            </template>
            <input 
              type="file" 
              ref="fileInput" 
              style="display: none;" 
              @change="handleFileChange"
              accept="audio/*,video/*" 
            />
          </div>
          <div class="meeting-name">
            <label for="meeting-name">{{ $t('meetingName') }}</label>
            <input 
              type="text" 
              id="meeting-name" 
              v-model="meetingName" 
              :placeholder="$t('meetingNamePlaceholder')" 
            />
          </div>
        </div>
        <div class="popup-footer">
          <button 
            class="upload-button" 
            @click="uploadFile" 
            :disabled="!selectedFile || !meetingName || isUploading"
          >
            {{ isUploading ? $t('uploading') : $t('uploadMeeting') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
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
    const { t } = useI18n();
    const showPopup = ref(false);
    const showUploadPopup = ref(false);
    const meetingToDelete = ref<Meeting | null>(null);
    const meetingName = ref('');
    const fileInput = ref<HTMLInputElement | null>(null);
    const selectedFile = ref<File | null>(null);
    const isFileSelected = ref(false);
    const isUploading = ref(false);

    const meetings = ref<Meeting[]>(Array.from({ length: 30 }, (_, i) => ({
      id: i + 1,
      date: `0${i + 1}.01.2023`,
      name: `Встреча ${i + 1}`,
      status: i % 2 === 0 ? 'new' : 'old',
      length: `${30 + i} мин`
    })));

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

    const closeUploadPopup = () => {
      showUploadPopup.value = false;
      selectedFile.value = null;
      isFileSelected.value = false;
      meetingName.value = '';
      isUploading.value = false;
    };

    const openFileDialog = () => {
      fileInput.value?.click();
    };

    const handleFileChange = (event: Event) => {
      const input = event.target as HTMLInputElement;
      if (input.files && input.files[0]) {
        const file = input.files[0];
        if (file.size > 1000 * 1024 * 1024) {
          alert(t('fileTooBig'));
          return;
        }
        selectedFile.value = file;
        isFileSelected.value = true;
      }
    };

    const handleDrop = (event: DragEvent) => {
      event.preventDefault();
      if (event.dataTransfer?.files.length) {
        const file = event.dataTransfer.files[0];
        if (file.size > 1000 * 1024 * 1024) {
          alert(t('fileTooBig'));
          return;
        }
        selectedFile.value = file;
        isFileSelected.value = true;
      }
    };

    const handleDragOver = (event: DragEvent) => {
      event.preventDefault();
    };

    const uploadFile = async () => {
      if (!selectedFile.value || !meetingName.value) {
        alert(t('selectFileAndName'));
        return;
      }

      isUploading.value = true;
      const formData = new FormData();
      formData.append('file', selectedFile.value);

      try {
        const response = await fetch('https://voiceflow.ru/api/transcribe', {
          method: 'POST',
          body: formData
        });

        if (response.status === 202) {
          // Файл успешно принят сервером
          meetings.value.unshift({
            id: meetings.value.length + 1,
            date: new Date().toLocaleDateString(),
            name: meetingName.value,
            status: 'new',
            length: t('processing')
          });
          closeUploadPopup(); // Закрываем попап
          return;
        }

        if (!response.ok) {
          throw new Error(t('serverError', { 
            status: response.status, 
            statusText: response.statusText 
          }));
        }

        const result = await response.json();
        
        const existingMeeting = meetings.value.find(m => m.name === meetingName.value);
        if (existingMeeting && result.segments.length > 0) {
          const lastSegment = result.segments[result.segments.length - 1];
          existingMeeting.length = `${Math.round(lastSegment.end / 60)} мин`;
        }

      } catch (error) {
        alert(t('uploadError', { 
          error: error instanceof Error ? error.message : t('unknownError')
        }));
      } finally {
        isUploading.value = false;
      }
    };


    return {
      goToHome,
      goToSettings,
      goToMeeting,
      meetings,
      showPopup,
      showUploadPopup,
      meetingToDelete,
      meetingName,
      fileInput,
      selectedFile,
      isFileSelected,
      isUploading,
      confirmDelete,
      deleteMeeting,
      cancelDelete,
      closeUploadPopup,
      openFileDialog,
      handleFileChange,
      handleDrop,
      handleDragOver,
      uploadFile
    };
  }
});
</script>

<style scoped src="@/assets/scss/MainView.scss"></style>
