<template>
  <header class="header" @click="handleOutsideClick">
    <div class="container">
      <!-- Header Top -->
      <div class="header__top-text">
        В∴С∴В∴А∴В<br />
        Объединенная Великая Ложа России<br />
        Д∴П∴Ш∴У∴
      </div>
      <div class="header__top">
        <div class="lodge-info" v-if="!isMobile">
          <h2 class="lodge-info__title">H∴L∴ A.S. Pushkin №9</h2>
          <p class="lodge-info__subtitle">Founded in Paris in 1991</p>
          <img src="@/assets/img/1.png" alt="Lodge Logo" class="lodge-info__logo" />
        </div>
        <div class="logo">
          <div class="logo__circle">
            <router-link to="/">
              <img src="@/assets/img/logo.png" alt="Lodge Logo" class="logo__image" />
            </router-link>
          </div>
          <!-- Conditional Text -->
          <div class="header__bottom-text">
            {{ isMobile ? 'Д∴Л∴ А.С. Пушкин №9' : 'United Grand Lodge of Russia 1921' }}
          </div>
        </div>
        <div class="lodge-info" v-if="!isMobile">
          <h2 class="lodge-info__title">Д∴Л∴ А.С. Пушкин №9</h2>
          <p class="lodge-info__subtitle">Основана в Париже 1991</p>
          <img src="@/assets/img/2.png" alt="Lodge Logo" class="lodge-info__logo" />
        </div>
      </div>
    </div>

    <!-- Navigation Menu -->
    <nav :class="['nav', { 'nav--fixed': isScrolled }]">
      <div class="container nav__container">
        <!-- Hamburger Menu -->
        <div class="hamburger" @click.stop="toggleNav">
          <span></span>
          <span></span>
          <span></span>
        </div>
        <!-- Logo in Fixed Nav -->
        <div class="nav__logo" v-if="isScrolled">
          <router-link to="/">
            <img src="@/assets/img/logo.png" alt="Lodge Logo" class="nav__logo-image" />
          </router-link>
        </div>
        <!-- Navigation List -->
        <ul :class="['nav__list', { active: isNavActive }]">
          <li class="nav__item" :class="{ 'nav__item--active': isDropdownActive }">
            <a class="nav__link" @click="toggleDropdown">
              Д:Л:. "ПУШКИН"
              <span class="chevron-down"></span>
            </a>
            <div class="dropdown" v-show="isDropdownActive">
              <router-link to="/pushkin/works" class="dropdown__item">ЗОДЧЕСКИЕ РАБОТЫ</router-link>
              <router-link to="/pushkin/history" class="dropdown__item">ИСТОРИЯ ЛОЖИ</router-link>
            </div>
          </li>
          <li class="nav__item">
            <a class="nav__link">
              МАСОНСТВО
              <span class="chevron-down"></span>
            </a>
            <div class="dropdown">
              <router-link to="/mason/principles" class="dropdown__item">ОБЩИЕ ПРИНЦИПЫ</router-link>
              <router-link to="/mason/symbols" class="dropdown__item">ГЛАВНЫЕ МАСОНСКИЕ СИМВОЛЫ</router-link>
              <router-link to="/mason/truth" class="dropdown__item">ПРАВДА/НЕПРАВДА О МАСОНСТВЕ</router-link>
            </div>
          </li>
          <li class="nav__item">
            <a class="nav__link">
              ВСТУПЛЕНИЕ
              <span class="chevron-down"></span>
            </a>
            <div class="dropdown">
              <router-link to="/join/form" class="dropdown__item">ФОРМА ВСТУПЛЕНИЯ</router-link>
            </div>
          </li>
          <li class="nav__item">
            <router-link to="/news" class="nav__link">НОВОСТИ</router-link>
          </li>
          <li class="nav__item">
            <router-link to="/ovlr" class="nav__link special">
              ОВЛР
              <span class="nav__subtext">1921</span>
            </router-link>
          </li>
          <li class="nav__item">
            <router-link to="/vlf" class="nav__link">ВЛФ</router-link>
          </li>
        </ul>
      </div>
    </nav>
  </header>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onUnmounted } from 'vue';

export default defineComponent({
  name: 'MainHeader',
  setup() {
    const isDropdownActive = ref(false);
    const isNavActive = ref(false);
    const isMobile = ref(false);
    const isScrolled = ref(false);
    const lastScrollTop = ref(0);

    const toggleDropdown = () => {
      isDropdownActive.value = !isDropdownActive.value;
    };

    const toggleNav = () => {
      isNavActive.value = !isNavActive.value;
    };

    const handleResize = () => {
      isMobile.value = window.innerWidth <= 768;
    };

    const handleScroll = () => {
      const currentScroll = window.scrollY;
      if (currentScroll > lastScrollTop.value && currentScroll > 310) {
        isScrolled.value = true;
      } else if (currentScroll < lastScrollTop.value && currentScroll <= 310) {
        isScrolled.value = false;
      }
      lastScrollTop.value = currentScroll;
    };

    const handleOutsideClick = (event: MouseEvent) => {
      if (isNavActive.value && !(event.target as HTMLElement).closest('.nav__list')) {
        isNavActive.value = false;
      }
    };

    onMounted(() => {
      handleResize();
      handleScroll();
      window.addEventListener('resize', handleResize);
      window.addEventListener('scroll', handleScroll);
      document.addEventListener('click', handleOutsideClick);
    });

    onUnmounted(() => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('scroll', handleScroll);
      document.removeEventListener('click', handleOutsideClick);
    });

    return {
      isDropdownActive,
      isNavActive,
      isMobile,
      isScrolled,
      toggleDropdown,
      toggleNav,
      handleOutsideClick,
    };
  },
});
</script>

<style scoped>
.hamburger {
  display: none;
}

.hamburger span {
  display: block;
  width: 25px;
  height: 3px;
  margin: 5px;
  background: var(--white);
}

.nav--fixed {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background: var(--primary);
  z-index: 1001;
  transition: background 0.3s ease;
}

.nav__logo {
  display: none;
}

.nav--fixed .nav__logo {
  display: block;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.nav__logo-image {
  height: 40px;
  margin-top: -5px;
}

@media (max-width: 768px) {
  .nav__list {
    display: none;
    flex-direction: column;
    gap: 30px;
    position: fixed;
    top: 0;
    left: 0;
    height: 100%;
    width: 70%;
    background: var(--primary);
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    z-index: 1000;
  }

  .nav__list.active {
    display: flex;
    transform: translateX(0);
  }

  .nav__link {
    text-align: left;
  }

  .nav__link.special {
    display: flex;
    align-items: center;
  }

  .hamburger {
    display: block;
    cursor: pointer;
    padding-left: 20px;
  }
}
</style>
