<template>
  <div class="main-container">
    <MainSidebar @navigateToMain="goToHome" />
    <div class="content">
      <div class="header">
        <h1>{{ t("accessGranting") }}</h1>
        <div class="account-info" @click="goToSettings" style="cursor: pointer">
          <div class="account-circle"></div>
          <span class="account-email">example@example.com</span>
        </div>
      </div>

      <div class="access-granting-content">
        <h2>{{ t("enterEmails") }}</h2>
        <div class="email-input-container">
          <textarea
            v-model="emails"
            placeholder="Введите почты через запятую или на каждой строке"
          ></textarea>
        </div>
        <button class="send-button" @click="sendEmails">{{ t("send") }}</button>

        <h2>{{ t("adminEmail") }}</h2>
        <div class="admin-email-container">
          <input
            type="email"
            v-model="adminEmail"
            placeholder="Введите почту администратора"
          />
        </div>
        <button class="send-button" @click="sendAdminEmail">
          {{ t("send") }}
        </button>
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
  name: "AccessGrantingView",
  components: {
    MainSidebar,
  },
  setup() {
    const { t } = useI18n();
    const router = useRouter();
    const goToHome = () => {
      router.push({ name: "MainView" });
    };

    const goToSettings = (event: Event) => {
      event.stopPropagation();
      router.push({ name: "SettingsView" });
    };

    const emails = ref("");
    const adminEmail = ref("");

    const sendEmails = () => {
      // Здесь можно добавить логику отправки введенных email
      alert(t("emailsSent"));
    };

    const sendAdminEmail = () => {
      // Здесь можно добавить логику отправки email администратора
      alert(t("adminEmailSent"));
    };

    return {
      t,
      goToHome,
      goToSettings,
      emails,
      adminEmail,
      sendEmails,
      sendAdminEmail,
    };
  },
});
</script>

<style scoped src="@/assets/scss/AccessGrantingView.scss"></style>
