<template>
  <footer class="footer">
    <div class="container">
      <div class="social">
        <a href="#" class="social__link">Соц сети</a>
        <a href="#" class="social__link">Соц сети</a>
        <a href="#" class="social__link">Соц сети</a>
      </div>
      <div class="copyright">
        <p>Copyright Д:.Л:. "А.С. Пушкин" №9</p>
        <p class="support">при поддержке Д:.Л:. «Северное Сияние» №2</p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts"></script>

<style scoped>
.footer {
  margin-top: 20px;
}

.social__link {
  text-decoration: none;
  color: #000;
  font-size: 16px;
}

.copyright {
  background-color: rgb(113, 113, 113);
  text-align: center;
  padding: 7px 0;
  margin-top: 20px;
}

.copyright p {
  color: white;
  margin: 0;
  font-size: 14px;
  font-weight: bold;
}

.copyright .support {
  color: white;
  font-size: 12px;
  font-weight: normal;
}
</style>
