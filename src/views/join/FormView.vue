<template>
  <div>
    <!-- Хедер -->
    <ThemeSwitcher />
    <Header />

    <!-- Main content -->
    <main class="main">
      <div class="container">
        <article class="form">
          <form @submit.prevent="handleSubmit" class="content-container">
            <header class="form-header">
              <h1 class="content-title">Вступление</h1>
            </header>

            <img src="@/assets/img/test.webp" alt="Article image" class="article__image" />

            <div class="content-text">
              <p>
                <span
                  style="
                    font-family:
                      book antiqua,
                      palatino,
                      serif;
                    font-size: 14pt;
                  "
                >
                  Уважаемый посетитель сайта! На этой странице нашего сайта Вы можете подать
                  прошение на вступление в ложу заполнив форму ниже. Перед заполнением формы
                  прошения о вступлении просим Вас внимательно ознакомиться с требованиями к
                  кандидатам и ограничениями.
                </span>
              </p>
              <p>
                <span
                  style="
                    font-family:
                      book antiqua,
                      palatino,
                      serif;
                    font-size: 14pt;
                  "
                >
                  Получив Ваше прошение, мы всегда исходим из того, что Вы делаете обдуманный шаг
                  чтобы стать масоном, вы прочитали требования к кандидатам, имеете представление о
                  том, чем масоны занимаются, принимаете масонские моральные ценности и правила.
                  Если у Вас остались к нам вопросы – Вы можете задать их с использованием наших
                  информационных ресурсов в Telegram.
                </span>
              </p>
              <p>
                <span
                  style="
                    font-family:
                      book antiqua,
                      palatino,
                      serif;
                    font-size: 14pt;
                  "
                >
                  После заполнения формы и отправки, с Вами свяжутся для обсуждения места и времени
                  первичного собеседования. В зависимости от загруженности братьев-собеседователей
                  на это может уйти до двух недель. Мы не уведомляем о получении и результатах
                  рассмотрения ваших прошений. В случае назначения Вам первичного собеседования,
                  порядок дальнейших действий Вам расскажет брат-собеседователь. Искренне желаем Вам
                  удачи!
                </span>
              </p>
            </div>

            <div class="form-fields">
              <div class="form-group" v-for="(field, index) in formFields" :key="index">
                <label class="form-label">{{ field.label }}</label>

                <!-- Текстовые и другие стандартные поля -->
                <input
                  v-if="field.type !== 'textarea' && field.type !== 'date'"
                  v-model="formData[field.name]"
                  :type="field.type"
                  class="form-input"
                  :required="field.required"
                />

                <!-- Текстовая область -->
                <textarea
                  v-if="field.type === 'textarea'"
                  v-model="formData[field.name]"
                  class="form-input"
                  :required="field.required"
                ></textarea>

                <!-- Поле даты -->
                <input
                  v-if="field.type === 'date'"
                  v-model="formData[field.name]"
                  type="date"
                  class="form-input"
                  :required="field.required"
                />
              </div>
            </div>

            <div class="checkbox-group">
              <h3 class="form-label">Подтверждаю, что:</h3>
              <div v-for="(checkbox, index) in checkboxes" :key="index" class="checkbox-container">
                <input
                  v-model="checkbox.checked"
                  type="checkbox"
                  class="checkbox-input"
                  :required="checkbox.required"
                />
                <label class="checkbox-label">{{ checkbox.label }}</label>
              </div>
            </div>

            <button type="submit" class="btn">Отправить форму</button>
          </form>
        </article>
      </div>
    </main>

    <!-- Футер -->
    <Footer />

    <!-- Кнопка для прокрутки вверх -->
    <ScrollTop />
  </div>
</template>

<script setup lang="ts">
import Header from '@/components/MainHeader.vue'
import Footer from '@/components/MainFooter.vue'
import ScrollTop from '@/components/ScrollTop.vue'
import ThemeSwitcher from '@/components/ThemeSwitcher.vue'
import { reactive } from 'vue'
import axios from 'axios';

type FormData = {
  fullName: string
  birthDate: string
  address: string
  phone: string
  email: string
  maritalStatus: string
  profession: string
  languages: string
  recommenders: string
  reason: string
  goals: string
  [key: string]: string | null
}

const formData = reactive<FormData>({
  fullName: '',
  birthDate: '',
  address: '',
  phone: '',
  email: '',
  maritalStatus: '',
  profession: '',
  languages: '',
  recommenders: '',
  reason: '',
  goals: '',
})

const formFields = [
  { label: 'Имя, отчество и фамилия', name: 'fullName', type: 'text', required: true },
  { label: 'Дата рождения', name: 'birthDate', type: 'date', required: true },
  {
    label: 'Адрес: почтовый индекс, город, область, страна',
    name: 'address',
    type: 'text',
    required: true,
  },
  { label: 'Контактный телефон', name: 'phone', type: 'tel', required: true },
  { label: 'Контактный адрес email', name: 'email', type: 'email', required: true },
  { label: 'Семейное положение', name: 'maritalStatus', type: 'select', required: true },
  { label: 'Профессия/род деятельности', name: 'profession', type: 'text', required: true },
  { label: 'Знание иностранных языков', name: 'languages', type: 'text', required: true },
  {
    label: 'Кто вас представляет / рекомендует? (имя, фамилия, № или имя Ложи)',
    name: 'recommenders',
    type: 'text',
    required: true,
  },
  {
    label:
      'Напишите несколько слов о том, почему вы решили подать прошение о вступлении в масонство',
    name: 'reason',
    type: 'textarea',
    required: true,
  },
  { label: 'Что вы ищете в масонстве?', name: 'goals', type: 'textarea', required: true },
]

const checkboxes = [
  {
    label: 'Судимости, в том числе снятой или погашенной, я не имею и не имел.',
    checked: false,
    required: true,
  },
  {
    label: 'Я имею возможность посещать собрания в Москве, не реже одного раза в месяц.',
    checked: false,
    required: true,
  },
  {
    label:
      'Добровольно без какого-либо принуждения передаю все данные этой анкеты для обработки с целью вступления в Братство Вольных каменщиков (масонов).',
    checked: false,
    required: true,
  },
  {
    label: 'Выражаю согласие с политикой конфиденциальности и обработки персональных данных',
    checked: false,
    required: true,
  },
]

const handleSubmit = async () => {
  try {
    const confirmations = checkboxes
      .filter((checkbox) => checkbox.checked)
      .map((checkbox) => checkbox.label);

    const payload = {
      ...formData,
      confirmations,
    };

    const response = await axios.post('https://lodgepushkin.com/api/admin/submit-form', payload);

    if (response.data.success) {
      alert('Форма успешно отправлена!');
    } else {
      alert('Ошибка при отправке формы. Пожалуйста, попробуйте снова.');
    }
  } catch (error) {
    console.error('Ошибка при отправке формы:', error);
    alert('Ошибка при отправке формы. Пожалуйста, попробуйте позже.');
  }
};
</script>

<style scoped src="@/assets/css/article.css"></style>
