<template>
  <div class="login-container">
    <div v-if="step === 1" class="form-container">
      <h2>{{ t('enterEmail') }}</h2>
      <p class="info-text">{{ t('emailInfo') }}</p>
      <input type="email" v-model="email" placeholder="Email" />
      <button @click="sendEmail">{{ t('send') }}</button>
    </div>
    <div v-else-if="step === 2" class="form-container">
      <h2>{{ t('createPassword') }}</h2>
      <input type="password" v-model="password" placeholder="Password" />
      <input type="password" v-model="confirmPassword" placeholder="Confirm Password" />
      <button @click="createPassword">{{ t('confirm') }}</button>
    </div>
    <div v-else-if="step === 3" class="form-container">
      <h2>{{ t('login') }}</h2>
      <input type="email" v-model="email" placeholder="Email" />
      <input type="password" v-model="password" placeholder="Password" />
      <button @click="login">{{ t('login') }}</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { setAuthenticated } from '@/router';

export default defineComponent({
  data() {
    return {
      step: 1,
      email: '',
      password: '',
      confirmPassword: ''
    };
  },
  setup() {
    const router = useRouter();
    const { t } = useI18n();
    return { router, t };
  },
  methods: {
    sendEmail() {
      // Logic to send email
      this.step = 2;
    },
    createPassword() {
      if (this.password === this.confirmPassword) {
        // Logic to create password
        this.step = 3;
      } else {
        alert("Passwords do not match");
      }
    },
    login() {
      // Logic to login
      setAuthenticated(true);
      this.router.push({ name: 'MainView' });
    }
  }
});
</script>

<style scoped src="@/assets/scss/LoginView.scss"></style>