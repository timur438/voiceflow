<template>
  <div class="form-container">
    <h2>{{ t('login') }}</h2>
    <input type="email" v-model="email" placeholder="Email" />
    <input type="password" v-model="password" placeholder="Password" />
    <button @click="login" :disabled="loading">{{ t('login') }}</button>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import axios from 'axios';

export default defineComponent({
  data() {
    return {
      email: '',
      password: '',
      loading: false,
      errorMessage: ''
    };
  },
  setup() {
    const router = useRouter();
    const { t } = useI18n();
    return { router, t };
  },
  methods: {
    async login() {
      this.loading = true;
      this.errorMessage = '';

      try {
        const response = await axios.post('https://voiceflow.ru/api/login', {
          email: this.email,
          password: this.password
        });

        if (response.data.access_token) {
          document.cookie = `access_token=${response.data.access_token}; path=/; Secure`;
          document.cookie = `decrypted_key=${response.data.key}; path=/; Secure`;
          this.router.push('/'); 
        }
      } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          this.errorMessage = error.response?.data?.detail || this.t('errorOccurred');
        } else {
          this.errorMessage = this.t('unexpectedError');
        }
      } finally {
        this.loading = false;
      }
    }
  }
});
</script>

<style scoped src="@/assets/scss/LoginView.scss"></style>