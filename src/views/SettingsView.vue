<template>
  <div class="main-container">
    <MainSidebar @navigateToMain="goToHome" />
    <div class="content">
      <div class="header">
        <h1>{{ t("mySettings") }}</h1>
        <div class="account-info" @click="goToSettings" style="cursor: pointer">
          <div class="account-circle"></div>
          <span class="account-email">example@example.com</span>
        </div>
      </div>
      <div class="settings-content">
        <h2>{{ t("autoRecord") }}</h2>
        <div class="auto-record-options">
          <label>
            <input type="radio" v-model="autoRecordOption" value="all" />
            {{ t("recordAll") }}
          </label>
          <label>
            <input type="radio" v-model="autoRecordOption" value="none" />
            {{ t("doNotRecord") }}
          </label>
        </div>
        <h2 class="language">{{ t("language") }}</h2>
        <div class="language-select">
          <select v-model="selectedLanguage" @change="changeLanguage">
            <option value="ru">Русский</option>
            <option value="en">English</option>
          </select>
        </div>
        <h2>{{ t("apiKey") }}</h2>
        <div class="api-key-container" @click="copyApiKey">
          <div class="api-key-input">
            <input type="text" v-model="apiKey" readonly />
            <button class="copy-button">
              <img src="@/assets/img/copy.svg" alt="Copy" class="copy-icon" />
            </button>
          </div>
          <button class="documentation-button">{{ t("documentation") }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import MainSidebar from "@/components/MainSidebar.vue";

export default defineComponent({
  name: "SettingsView",
  components: {
    MainSidebar,
  },
  setup() {
    const { t, locale } = useI18n();
    const router = useRouter();
    const goToHome = () => {
      router.push({ name: "MainView" });
    };

    const goToSettings = (event: Event) => {
      event.stopPropagation();
      router.push({ name: "SettingsView" });
    };

    const autoRecordOption = ref("all");
    const selectedLanguage = ref("ru");
    const apiKey = ref("1234-5678-ABCD-EFGH");

    const changeLanguage = () => {
      locale.value = selectedLanguage.value;
    };

    const copyApiKey = () => {
      navigator.clipboard.writeText(apiKey.value);
      alert(t("copied"));
    };

    return {
      t,
      goToHome,
      goToSettings,
      autoRecordOption,
      selectedLanguage,
      apiKey,
      changeLanguage,
      copyApiKey,
    };
  },
});
</script>

<style scoped src="@/assets/scss/SettingsView.scss"></style>
