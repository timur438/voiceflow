<template>
  <div class="home">
    <!-- Хедер -->
    <ThemeSwitcher />
    <Header />

    <!-- Основной контент -->
    <main class="main">
      <div class="container">
        <!-- Приветственное сообщение -->
        <section class="welcome">
          <div class="welcome__content">
            <h3 class="welcome__title">ПРИВЕТСТВЕННОЕ СООБЩЕНИЕ</h3>
            <h2 class="welcome__heading">
              Приветствие Досточтимого Мастера<br />
              Достопочтенной Ложи «А.С. Пушкин»
            </h2>
            <p class="welcome__text">Приветствуем Вас на сайте Достопочтенной Ложи «А.С. Пушкин» (город Барселона), одной из старейших масонских организаций современной России!</p>
            <router-link :to="`/article/hello`" custom v-slot="{ navigate }">
              <button class="btn btn--outline" @click="navigate">Подробнее</button>
            </router-link>
          </div>
          <img src="@/assets/img/hello.jpg" class="welcome__image"/>
        </section>

        <!-- Новости -->
        <section class="section">
          <div class="section__header">
            <h2 class="section__title">МАСОНСТВО / Рекомендованная литература</h2>
            <div class="section__line"></div>
          </div>
          <div class="news-grid">
            <!-- Проверяем, есть ли последняя новость -->
            <article class="news-card" v-if="latestNews">
              <div class="news-card__image">
                <img :src="latestNews.coverImage" alt="News Image" class="news-card__icon" />
              </div>
              <div class="news-card__content">
                <span class="news-card__label">НОВОСТИ</span>
                <h3 class="news-card__title">{{ latestNews.title }}</h3>
                <p class="news-card__text">{{ latestNews.content }}</p>
                <router-link :to="`/article/${latestNews.id}`" custom v-slot="{ navigate }">
                  <button class="btn btn--outline" @click="navigate">Подробнее</button>
                </router-link>
              </div>
            </article>
            <!-- Если новости нет -->
            <p v-else>Новости не найдены.</p>
          </div>
        </section>

        <!-- Мероприятия -->
        <section class="section">
          <div class="section__header">
            <h2 class="section__title">МАСОНСТВО / ПОСЛЕДНИЕ МЕРОПРИЯТИЯ</h2>
            <div class="section__line"></div>
          </div>
          <div class="events-grid">
            <div class="event-card event-card--side">
              <img src="@/assets/img/history.png" alt="Event Image" class="event-card__image" />
              <div class="event-card__overlay">
                <h3 class="event-card__title">История Ложи</h3>
                <router-link :to="`/pushkin/history`" custom v-slot="{ navigate }">
                  <button class="btn" @click="navigate">Подробнее</button>
                </router-link>
              </div>
            </div>
            <div class="event-card event-card--side">
              <img src="@/assets/img/principles.png" alt="Event Image" class="event-card__image" />
              <div class="event-card__overlay">
                <h3 class="event-card__title">Общие принципы</h3>
                <router-link :to="`/mason/principles`" custom v-slot="{ navigate }">
                  <button class="btn" @click="navigate">Подробнее</button>
                </router-link>
              </div>
            </div>
            <div class="event-card event-card--center">
              <img src="@/assets/img/symbols/header.jpg" alt="Event Image" class="event-card__image" />
              <div class="event-card__overlay">
                <h3 class="event-card__title">Главные масонские символы</h3>
                <router-link :to="`/mason/symbols`" custom v-slot="{ navigate }">
                  <button class="btn" @click="navigate">Подробнее</button>
                </router-link>
              </div>
            </div>
            <div class="event-card event-card--side">
              <img src="@/assets/img/truth.webp" alt="Event Image" class="event-card__image" />
              <div class="event-card__overlay">
                <h3 class="event-card__title">Правда/Неправда о масонстве</h3>
                <router-link :to="`/mason/truth`" custom v-slot="{ navigate }">
                  <button class="btn" @click="navigate">Подробнее</button>
                </router-link>
              </div>
            </div>
            <div class="event-card event-card--side">
              <img src="@/assets/img/test.webp" alt="Event Image" class="event-card__image" />
              <div class="event-card__overlay">
                <h3 class="event-card__title">Вступление в Братство</h3>
                <router-link :to="`/join/form`" custom v-slot="{ navigate }">
                  <button class="btn" @click="navigate">Подробнее</button>
                </router-link>
              </div>
            </div>
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
import { ref, onMounted } from 'vue'
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

const latestNews = ref<NewsItem | null>(null)

const fetchLatestNews = async () => {
  try {
    const response = await axios.get('https://lodgepushkin.com/api/news/get');

    const filteredNews = response.data.filter(
      (news: NewsItem) =>
        Number(news.categoryID) === 2 && news.date && !isNaN(new Date(news.date).getTime())
    );

    const sortedNews = filteredNews.sort(
      (a: NewsItem, b: NewsItem) => new Date(b.date).getTime() - new Date(a.date).getTime()
    );

    if (sortedNews.length > 0) {
      const news = sortedNews[0];
      latestNews.value = {
        ...news,
        coverImage: `https://lodgepushkin.com/api/news${news.coverImage}`,
        content: stripHtmlAndLimitWords(news.content, 20),
      };
    }
  } catch (error) {
    console.error('Ошибка при получении последней новости:', error);
  }
};

onMounted(fetchLatestNews)
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
.event-card__image {
  width: 100%;
  height: auto;
  object-fit: contain;
  display: block;
}
</style>
