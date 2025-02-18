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
      <div class="meeting-content">
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
              В ходе встречи сооснователь сервиса mymeet.ai, Илья, представил
              функционал и преимущества продукта, который автоматизирует процесс
              записи и анализа встреч. Основное внимание было уделено тому, как
              mymeet.ai помогает пользователям, включая руководителей,
              исследователей и отделы продаж, экономить время и улучшать
              качество работы. Обсуждались новые функции, такие как
              персонализированные шаблоны отчетов и интеграция с различными
              платформами. В завершение встречи были определены дальнейшие шаги
              по развитию продукта и его функциональности.
            </p>
          </div>
          <div class="summary-block">
            <h3>Саммари по темам:</h3>
            <p><strong>Функционал mymeet.ai</strong></p>
            <ul>
              <li>
                Автоматически подключается к Google-календарю и записывает
                встречи в Zoom, Google Meet, СалютJazz, Яндекс.Телемост и
                TrueConf, предоставляя отчет по встрече через 3 минуты после
                завершения.
              </li>
              <li>
                Поддерживает загрузку аудио и видео файлов до 1 Гб, что
                позволяет пользователям легко интегрировать записи встреч.
              </li>
            </ul>
            <p><strong>Целевая аудитория и сегменты пользователей</strong></p>
            <ul>
              <li>
                Руководители и проджект-менеджеры: Экономят время на написание
                фоллоу-апов и минутов, могут быстро ознакомиться с записями
                встреч, если отсутствовали.
              </li>
              <li>
                Исследователи и социологи: Упрощают процесс расшифровки интервью
                и выделения инсайтов.
              </li>
              <li>
                Отделы продаж: Используют amoCRM-виджет для интеграции с CRM и
                автоматизации записи встреч.
              </li>
            </ul>
            <p><strong>Новые функции и улучшения</strong></p>
            <ul>
              <li>
                В сентябре планируется внедрение персонализированных шаблонов
                отчетов, адаптированных под разные профессии (Sales, HR,
                исследователи).
              </li>
              <li>
                Разработка чата для взаимодействия с отчетами, что позволит
                пользователям задавать вопросы по содержанию встреч.
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useI18n } from "vue-i18n";
import MainSidebar from "@/components/MainSidebar.vue";

interface Participant {
  name: string;
  color: string;
}

interface Meeting {
  id: number;
  date: string;
  name: string;
  status: "new" | "old";
  length: string;
  keywords: string[];
  participants: Participant[];
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
    const goToHome = () => {
      router.push({ name: "MainView" });
    };

    const goToSettings = (event: Event) => {
      event.stopPropagation();
      router.push({ name: "SettingsView" });
    };

    const meeting = ref<Meeting>({
      id: Number(route.params.id),
      date: "01.01.2023",
      name: `Встреча ${route.params.id}`,
      status: "new",
      length: "30 мин",
      keywords: ["ключевое слово 1", "ключевое слово 2", "ключевое слово 3"],
      participants: [
        { name: "Участник 1", color: "#8A2BE2" },
        { name: "Участник 2", color: "#9370DB" },
        { name: "Участник 3", color: "#BA55D3" },
      ],
    });

    const activeTab = ref("transcript");

    return { t, goToHome, goToSettings, meeting, activeTab };
  },
});
</script>

<style scoped src="@/assets/scss/MeetingView.scss"></style>
