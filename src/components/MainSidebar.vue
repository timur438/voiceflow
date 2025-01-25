<template>
  <aside class="sidebar">
    <div class="sidebar-content">
      <div class="logo" @click="goToHome">
        <div class="logo-box"></div>
        <button class="logo-button">Whisper</button>
      </div>
      <nav class="menu">
        <ul>
          <li>
            <router-link to="/" @click="goToHome">
              <img src="@/assets/img/category.svg" alt="My Meetings" />
              {{ $t('myMeetings') }}
            </router-link>
          </li>
          <li>
            <router-link to="/settings">
              <img src="@/assets/img/setting.svg" alt="Settings and Integrations" />
              {{ $t('settingsAndIntegrations') }}
            </router-link>
          </li>
          <li><a href="#"><img src="@/assets/img/logout.svg" alt="Logout" />{{ $t('logout') }}</a></li>
        </ul>
      </nav>
    </div>
  </aside>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'MainSidebar',
  setup() {
    const router = useRouter();
    const goToHome = () => {
      router.push({ name: 'MainView' });
    };
    return { goToHome };
  }
});
</script>

<style scoped src="@/assets/scss/MainSidebar.scss"></style>
