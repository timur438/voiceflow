<template>
  <div class="form-container">
    <h2>{{ t('createPassword') }}</h2>
    <input type="password" v-model="password" placeholder="Password" />
    <input type="password" v-model="confirmPassword" placeholder="Confirm Password" />
    <button @click="createPassword">{{ t('confirm') }}</button>
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
        const email = this.route.query.email as string;

        console.log("Token:", token);
        console.log("Email:", email);

        const response = await axios.post(
          'https://voiceflow.ru/api/register',
          {
            token,
            email,
            password: this.password,
          },
          {
            headers: {
              'Content-Type': 'application/json',
            },
          }
        );

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