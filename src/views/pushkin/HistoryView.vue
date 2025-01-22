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
            <div class="content-category">Д:Л:. "ПУШКИН</div>
            <h1 class="content-title">История Ложи</h1>
          </header>

          <img src="@/assets/img/test.webp" alt="Article image" class="article__image" />

          <h2 class="content-subtitle">ПРИМЕР ТЕКСТА ОГЛАВЛЕНИЯ</h2>

          <div class="content-text">
            <p>
              Lorem ipsum odor amet, consectetuer adipiscing elit. Enim aptent curae ullamcorper
              scelerisque amet aptent orci. Non in auctor accumsan lectus neque dolor nisi enim.
              Arcu dolor posuere; scelerisque libero ut laoreet. Magnis erat inceptos dignissim
              dictumst torquent aenean non sociosqu senectus.
            </p>
            <p>
              Ligula tortor nulla habitasse accumsan taciti. Cras ex dictum donec efficitur diam
              vivamus vehicula pellentesque. Ut tortor eget cras venenatis amet penatibus.
            </p>
            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusantium nulla delectus
              reprehenderit voluptatibus sequi porro architecto quam excepturi quasi dicta,
              voluptatum necessitatibus laborum unde culpa nesciunt suscipit incidunt deleniti
              labore?
            </p>
          </div>
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
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css');
@import url('https://fonts.googleapis.com/css2?family=Baskervville:ital@0;1&family=Montserrat:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');

@import '@/assets/css/style.css';
@import '@/assets/css/article.css';
</style>
