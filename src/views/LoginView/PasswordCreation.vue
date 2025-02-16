<template>
  <div class="login-container">
    <div class="form-container">
      <h2>{{ t('createPassword') }}</h2>

      <p class="password-text">
        {{ t('passwordComplexityInfo') }}
      </p>
      <p class="password-text">
        {{ t('lostPasswordWarning') }}
      </p>

      <div class="password-container">
        <input type="password" v-model="password" :placeholder="t('password')" />
        <input type="password" v-model="confirmPassword" :placeholder="t('confirmPassword')" />
      </div>
      <button @click="createPassword" :disabled="loading">{{ t('confirm') }}</button>
    
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useI18n } from 'vue-i18n';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router';

export default defineComponent({
  data() {
    return {
      password: '',
      confirmPassword: '',
      loading: false,
      errorMessage: ''
    };
  },
  setup() {
    const { t } = useI18n();
    const router = useRouter();
    const route = useRoute();
    return { t, router, route };
  },
  methods: {
    async createPassword() {
      if (this.password !== this.confirmPassword) {
        alert(this.t('passwordMismatch'));
        return;
      }

      this.loading = true;
      this.errorMessage = '';

      try {
        const token = this.route.query.token as string;

        console.log("Token:", token);

        await axios.post(
          'https://voiceflow.ru/api/register',
          {
            token,
            password: this.password,
          },
          {
            headers: {
              'Content-Type': 'application/json',
            },
          }
        );

        // Перенаправляем на страницу входа без сохранения куков
        this.router.push('/login'); 

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