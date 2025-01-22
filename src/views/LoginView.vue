<template>
  <div class="login-container">
    <div v-if="step === 1" class="form-container">
      <h2>Введите ваш email</h2>
      <p class="info-text">Если почта найдется в нашей базе, на нее придет письмо.</p>
      <input type="email" v-model="email" placeholder="Email" />
      <button @click="sendEmail">Отправить</button>
    </div>
    <div v-else-if="step === 2" class="form-container">
      <h2>Создайте и подтвердите ваш пароль</h2>
      <input type="password" v-model="password" placeholder="Пароль" />
      <input type="password" v-model="confirmPassword" placeholder="Подтвердите пароль" />
      <button @click="createPassword">Подтвердить</button>
    </div>
    <div v-else-if="step === 3" class="form-container">
      <h2>Вход</h2>
      <input type="email" v-model="email" placeholder="Email" />
      <input type="password" v-model="password" placeholder="Пароль" />
      <button @click="login">Войти</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';

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
    return { router };
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
        alert("Пароли не совпадают");
      }
    },
    login() {
      // Logic to login
      this.router.push({ name: 'MainView' });
    }
  }
});
</script>

<style scoped src="@/assets/scss/LoginView.scss"></style>
