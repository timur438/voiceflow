<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useI18n } from "vue-i18n";
import MainSidebar from "@/components/MainSidebar.vue";

interface Participant {
  name: string;
  color: string;
}

interface Meeting {
  id: string;
  date: string;
  name: string;
  status: "new" | "old";
  length: string;
  keywords: string[];
  participants: Participant[];
  transcript?: string;
  summary?: string;
}

export default defineComponent({
  name: "MeetingView",
  components: {
    MainSidebar,
  },
  setup() {
    const { t } = useI18n();
    const router = useRouter();
    const route = useRoute();
    const meeting = ref<Meeting | null>(null);
    const activeTab = ref("transcript");

    const goToHome = () => {
      router.push({ name: "MainView" });
    };

    const goToSettings = (event: Event) => {
      event.stopPropagation();
      router.push({ name: "SettingsView" });
    };

    const loadMeeting = () => {
      const savedTranscripts = localStorage.getItem("transcripts");
      if (savedTranscripts) {
        const meetings: Meeting[] = JSON.parse(savedTranscripts);
        const foundMeeting = meetings.find((m) => m.id === route.params.id);
        if (foundMeeting) {
          meeting.value = foundMeeting;
        } else {
          router.push({ name: "MainView" });
        }
      } else {
        router.push({ name: "MainView" });
      }
    };

    onMounted(loadMeeting);

    return { t, goToHome, goToSettings, meeting, activeTab };
  },
});
</script>

<template>
  <div class="main-container">
    <MainSidebar @navigateToMain="goToHome" />
    <div class="content">
      <div class="header">
        <div class="back" @click="goToHome">
          <img src="@/assets/img/back-arrow.svg" alt="Back" class="back-icon" />
          <span>{{ t("back") }}</span>
        </div>
        <div class="account-info">
          <span class="share">{{ t("share") }}</span>
          <span class="export">{{ t("export") }}</span>
          <div
            class="account-circle"
            @click="goToSettings"
            style="cursor: pointer"
          ></div>
          <span
            class="account-email"
            @click="goToSettings"
            style="cursor: pointer"
            >example@example.com</span
          >
        </div>
      </div>
      <div v-if="meeting" class="meeting-content">
        <h1 class="meeting-title">{{ meeting.name }}</h1>
        <div class="meeting-details">
          <div class="detail-item">
            <img
              src="@/assets/img/frame.svg"
              alt="Uploaded"
              class="detail-icon"
            />
            {{ t("uploaded") }}
          </div>
          <div class="detail-item">
            <img
              src="@/assets/img/calendar.svg"
              alt="Date"
              class="detail-icon"
            />
            {{ meeting.date }}
          </div>
          <div class="detail-item">{{ meeting.length }}</div>
        </div>
        <div class="keywords-section">
          <h2>{{ t("keywords") }}</h2>
          <p class="keywords">{{ meeting.keywords.join(", ") }}</p>
        </div>
        <div class="participants-section">
          <h2>
            {{ t("participants") }}
            <img src="@/assets/img/lamp.svg" alt="Lamp" class="lamp-icon" />
          </h2>
          <p class="participants">
            <span
              v-for="(participant, index) in meeting.participants"
              :key="index"
              :style="{ color: participant.color }"
            >
              {{ participant.name
              }}<span v-if="index < meeting.participants.length - 1">, </span>
            </span>
          </p>
        </div>
        <div class="meeting-header">
          <div class="tabs">
            <span
              class="tab"
              :class="{ active: activeTab === 'transcript' }"
              @click="activeTab = 'transcript'"
              >{{ t("transcript") }}</span
            >
            <span
              class="tab"
              :class="{ active: activeTab === 'summary' }"
              @click="activeTab = 'summary'"
              >{{ t("summary") }}</span
            >
          </div>
          <img src="@/assets/img/copy.svg" alt="Copy" class="copy-icon" />
        </div>
        <div class="separator"></div>
        <div v-if="activeTab === 'summary'" class="summary-content">
          <div class="summary-block">
            <h3>Супер краткое содержание:</h3>
            <p>
              {{ meeting.summary || "Нет данных" }}
            </p>
          </div>
        </div>
      </div>
      <div v-else>
        <p>Загрузка данных...</p>
      </div>
    </div>
  </div>
</template>

<style scoped src="@/assets/scss/MeetingView.scss"></style>