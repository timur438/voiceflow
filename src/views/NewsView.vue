<template>
  <div class="news-view">
    <!-- Хедер -->
    <ThemeSwitcher />
    <Header />

    <!-- Main Content -->
    <main class="main">
      <div class="container">
        <section class="section">
          <div class="section__header">
            <h2 class="section__title">МАСОНСТВО / НОВОСТИ</h2>
            <div class="section__line"></div>
          </div>

          <div class="news-grid">
            <!-- Отображение новостей -->
            <article
              v-for="news in paginatedNews"
              :key="news._id"
              class="news-card"
            >
              <div class="news-card__image">
                <img :src="news.coverImage" alt="News Image" class="news-card__icon" />
              </div>
              <div class="news-card__content">
                <span class="news-card__label">НОВОСТИ</span>
                <h3 class="news-card__title">{{ news.title }}</h3>
                <p class="news-card__text">{{ news.content }}</p>
                <router-link :to="`/article/${news.id}`" custom v-slot="{ navigate }">
                  <button class="btn" @click="navigate">Подробнее</button>
                </router-link>
              </div>
            </article>
          </div>

          <!-- Пагинация -->
          <div class="pagination">
            <button
              class="btn pg--btn--outline"
              :disabled="currentPage === 1"
              @click="prevPage"
            >
              Назад
            </button>
            <span>Страница {{ currentPage }} из {{ totalPages }}</span>
            <button
              class="btn pg--btn--outline"
              :disabled="currentPage === totalPages"
              @click="nextPage"
            >
              Вперед
            </button>
          </div>
        </section>
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
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

// Интерфейс для объекта новости
interface NewsItem {
  _id: string
  id: number
  title: string
  content: string
  categoryID: number
  coverImage: string
  date: string
}

const stripHtmlAndLimitWords = (html: string, wordLimit: number): string => {
  const plainText = html.replace(/<\/?[^>]+>/g, ' ').replace(/\s+/g, ' ').trim()

  const words = plainText.split(/\s+/).slice(0, wordLimit)

  return words.join(' ') + (words.length === wordLimit ? '...' : '')
}

const newsList = ref<NewsItem[]>([])
const currentPage = ref(1) // Текущая страница
const itemsPerPage = 10 // Количество новостей на страницу

// Вычисляем общее количество страниц
const totalPages = computed(() => Math.ceil(newsList.value.length / itemsPerPage))

// Фильтруем новости для текущей страницы
const paginatedNews = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return newsList.value.slice(start, end)
})

// Переключение страниц
const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const fetchNews = async () => {
  try {
    const response = await axios.get('https://lodgepushkin.com/api/news/get');

    const today = new Date(); 

    const filteredNews = response.data
      .filter((news: NewsItem) => {
        const isCorrectCategory = Number(news.categoryID) === 2;

        const newsDate = new Date(news.date);

        const isDateValid = newsDate <= today;

        return isCorrectCategory && isDateValid;
      })
      .map((news: NewsItem) => ({
        ...news,
        coverImage: `https://lodgepushkin.com/api/news${news.coverImage}`,
        content: stripHtmlAndLimitWords(news.content, 20),
      }));

    newsList.value = filteredNews
  } catch (error) {
    console.error('Ошибка при получении новостей:', error)
  }
}

// Получаем новости при монтировании компонента
onMounted(fetchNews)
</script>

<style scoped>
@import '@/assets/css/style.css';
@import '@/assets/css/article.css';

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 20px;
}
.news-card__image img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}
</style>
