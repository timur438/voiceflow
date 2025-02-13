<template>
  <div class="form-container">
    <h2>{{ t('enterEmail') }}</h2>
    <p class="info-text">{{ t('emailInfo') }}</p>
    <input type="email" v-model="email" placeholder="Email" />
    <button @click="sendEmail" :disabled="loading">
      {{ loading ? t('loading') : t('send') }}
    </button>
    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useI18n } from 'vue-i18n';
import axios from 'axios';

export default defineComponent({
  data() {
    return {
      email: '',
      loading: false,
      message: '',
    };
  },
  setup() {
    const { t } = useI18n();
    return { t };
  },
  methods: {
    async sendEmail() {
      this.loading = true;
      this.message = '';

      try {
        const response = await axios.post('/api/check', { email: this.email });

        if (response.data.redirect) {
          this.$router.push({ path: '/login', query: { email: this.email } });
        } else {
          this.message = this.t('checkEmail');
        }
      } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          this.message = error.response?.data?.detail || this.t('errorOccurred');
        } else {
          this.message = this.t('unexpectedError');
        }
      } finally {
        this.loading = false;
      }
    }
  }
});
</script>

<style scoped src="@/assets/scss/LoginView.scss"></style>