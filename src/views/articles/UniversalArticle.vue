<template>
  <div>
    <!-- Хедер -->
    <ThemeSwitcher />
    <Header />

    <!-- Main content -->
    <main class="main">
      <div class="container">
        <article class="content-container">
          <header>
            <!-- Динамическое название подраздела в зависимости от categoryID -->
            <div class="content-category">{{ categoryTitle }}</div>
            <h1 class="content-title">{{ article.title }}</h1>
          </header>

          <img :src="article.coverImage" alt="Article image" class="article__image" />

          <div class="content-text" v-html="article.content"></div> <!-- Вставляем HTML контент -->
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
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import Header from '@/components/MainHeader.vue'
import Footer from '@/components/MainFooter.vue'
import ScrollTop from '@/components/ScrollTop.vue'
import ThemeSwitcher from '@/components/ThemeSwitcher.vue'

const article = ref({
  title: '',
  content: '',
  coverImage: '',
  categoryID: 0 // Добавляем categoryID
})

// Переменная для хранения названия подраздела
const categoryTitle = ref('')

// Получаем ID статьи из URL
const route = useRoute()
const articleId = route.params.id

const fetchArticle = async () => {
  try {
    const response = await axios.get(`https://lodgepushkin.com/api/news/get/${articleId}`)
    const fetchedArticle = response.data

    article.value = {
      title: fetchedArticle.title,
      content: fetchedArticle.content,
      coverImage: `https://lodgepushkin.com/api/news${fetchedArticle.coverImage}`,
      categoryID: fetchedArticle.categoryID
    }

    // Устанавливаем название подраздела в зависимости от categoryID
    categoryTitle.value = article.value.categoryID === 1 ? 'ЗОДЧЕСКИЕ РАБОТЫ' : 'НОВОСТИ'
  } catch (error) {
    console.error('Ошибка при получении статьи:', error)
  }
}

onMounted(fetchArticle)
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css');
@import url('https://fonts.googleapis.com/css2?family=Baskervville:ital@0;1&family=Montserrat:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');

@import '@/assets/css/style.css';
@import '@/assets/css/article.css';
</style>
