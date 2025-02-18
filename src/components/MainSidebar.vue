<template>
  <aside class="sidebar">
    <div class="sidebar-content">
      <div class="logo" @click="goToHome">
        <div class="logo-box"></div>
        <button class="logo-button">Voiceflow</button>
      </div>
      <nav class="menu">
        <ul>
          <li>
            <router-link to="/" @click="goToHome">
              <img src="@/assets/img/category.svg" alt="My Meetings" />
              {{ $t("myMeetings") }}
            </router-link>
          </li>
          <li>
            <router-link to="/settings">
              <img
                src="@/assets/img/setting.svg"
                alt="Settings and Integrations"
              />
              {{ $t("settingsAndIntegrations") }}
            </router-link>
          </li>
          <li>
            <a href="#" @click.prevent="logout"
              ><img src="@/assets/img/logout.svg" alt="Logout" />{{
                $t("logout")
              }}</a
            >
          </li>
        </ul>
      </nav>
    </div>
  </aside>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useRouter } from "vue-router";

export default defineComponent({
  name: "MainSidebar",
  setup() {
    const router = useRouter();
    const goToHome = () => {
      router.push({ name: "MainView" });
    };
    const logout = () => {
      if (confirm("Вы действительно хотите выйти?")) {
        document.cookie =
          "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        document.cookie =
          "decrypted_key=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        document.cookie =
          "email=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        router.push("/login");
      }
    };
    return { goToHome, logout };
  },
});
</script>

<style scoped src="@/assets/scss/MainSidebar.scss"></style>
