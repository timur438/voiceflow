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
          <span class="account-email">{{ accountEmail }}</span>
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
          <div class="meeting-details">
            <div class="meeting-name">
              <label for="meeting-name">{{ $t('meetingName') }}</label>
              <input 
                type="text" 
                id="meeting-name" 
                v-model="meetingName" 
                :placeholder="$t('meetingNamePlaceholder')" 
              />
            </div>
            <div class="speaker-count">
              <label for="speaker-count">{{ $t('speakerCount') }}</label>
              <input 
                type="number" 
                id="speaker-count" 
                v-model.number="speakerCount" 
                min="1"
                required
                :placeholder="$t('speakerCountPlaceholder')"
              />
            </div>
          </div>
        </div>
        <div class="popup-footer">
          <button 
            class="upload-button" 
            @click="uploadFile" 
            :disabled="!isFormValid || isUploading"
          >
            {{ isUploading ? $t('uploading') : $t('uploadMeeting') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import MainSidebar from '@/components/MainSidebar.vue';
import { decryptTranscriptData, getAccessToken, getDecryptedKey } from '@/utils/crypto';
import axios from 'axios';

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
    const speakerCount = ref<number | null>(null);
    const fileInput = ref<HTMLInputElement | null>(null);
    const selectedFile = ref<File | null>(null);
    const isFileSelected = ref(false);
    const isUploading = ref(false);

    const meetings = ref<Meeting[]>([]);

    const isFormValid = computed(() => {
      return selectedFile.value && meetingName.value && speakerCount.value && speakerCount.value > 0;
    });

    const getItemFromLocalStorage = (name: string) => {
      const item = localStorage.getItem(name);
      try {
        return item ? JSON.parse(item) : item;
      } catch (e) {
        console.error(`Ошибка при парсинге локального хранилища для '${name}':`, e);
        return item;
      }
    };

    const accountEmail = ref(getItemFromLocalStorage('email') || 'unknown@example.com');

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
      speakerCount.value = null;
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
        const fileName = file.name.replace(/\.[^/.]+$/, "");
        meetingName.value = fileName;
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
        const fileName = file.name.replace(/\.[^/.]+$/, "");
        meetingName.value = fileName;
      }
    };

    const handleDragOver = (event: DragEvent) => {
      event.preventDefault();
    };

    const uploadFile = async () => {
      if (!selectedFile.value || !meetingName.value || !speakerCount.value) {
        alert(t('selectFileAndName'));
        return;
      }
      
      isUploading.value = true;
      const formData = new FormData();
      formData.append('file', selectedFile.value);
      formData.append('speaker_count', speakerCount.value.toString());
      formData.append('meeting_name', meetingName.value.toString());
      
      const decryptedKey = getDecryptedKey();
      if (decryptedKey) {
        formData.append('decrypted_key', decryptedKey); 
      } else {
        alert(t('missingKey'));
        isUploading.value = false;
        return;
      }

      const accessToken = document.cookie.split('; ').find(row => row.startsWith('access_token='))?.split('=')[1];
      if (!accessToken) {
        alert(t('missingToken'));
        isUploading.value = false;
        return;
      }

      try {
        const response = await axios.post('https://voiceflow.ru/api/transcribe', formData, {
          headers: {
            Authorization: `Bearer ${accessToken}`
          }
        });

        if (response.status === 202) {
          meetings.value.unshift({
            id: meetings.value.length + 1,
            date: new Date().toLocaleDateString(),
            name: meetingName.value,
            status: 'new',
            length: t('processing')
          });
          closeUploadPopup();
          return;
        }

        throw new Error(t('serverError', { 
          status: response.status, 
          statusText: response.statusText 
        }));
      } catch (error) {
        alert(t('uploadError', { 
          error: error instanceof Error ? error.message : t('unknownError')
        }));
      } finally {
        isUploading.value = false;
      }
    };

    const loadTranscripts = async () => {
      const token = getAccessToken();
      const key = getDecryptedKey();

      if (!token || !key) {
        console.log("Token or key is missing.");
        return;
      }

      try {
        const response = await axios.get('https://voiceflow.ru/api/transcripts', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.status === 200) {
          const { transcripts } = response.data;
          console.log("Received Transcripts:", transcripts);

          const decryptedTranscripts = transcripts.map((encryptedData: string) => {
            const decrypted = decryptTranscriptData(encryptedData, key);
            console.log("Decrypted Transcript:", decrypted);
            return decrypted;
          });

          localStorage.setItem('transcripts', JSON.stringify(decryptedTranscripts));
          meetings.value = decryptedTranscripts;
        } else {
          console.error("Failed to fetch transcripts:", response.statusText);
        }
      } catch (error) {
        console.error("Error fetching transcripts:", error);
      }
    };

    onMounted(loadTranscripts);

    return {
      goToHome,
      goToSettings,
      goToMeeting,
      meetings,
      showPopup,
      showUploadPopup,
      meetingToDelete,
      meetingName,
      speakerCount,
      fileInput,
      selectedFile,
      isFileSelected,
      isUploading,
      isFormValid,
      confirmDelete,
      deleteMeeting,
      cancelDelete,
      closeUploadPopup,
      openFileDialog,
      handleFileChange,
      handleDrop,
      handleDragOver,
      uploadFile,
      accountEmail
    };
  }
});
</script>

<style scoped src="@/assets/scss/MainView.scss"></style>