export function initializeThemeAndMenu(): void {
  const hamburger = document.querySelector('.hamburger') as HTMLElement
  const navList = document.querySelector('.nav__list') as HTMLElement

  hamburger.addEventListener('click', () => {
    navList.classList.toggle('active')
    hamburger.classList.toggle('active')
  })

  document.addEventListener('click', (e: MouseEvent) => {
    const target = e.target as HTMLElement | null
    if (target && !target.closest('.nav')) {
      navList.classList.remove('active')
      hamburger.classList.remove('active')
    }
  })

  const themeSwitcherHTML = `
      <button class="theme-switcher" aria-label="Переключить тему">
          <svg class="sun-and-moon" aria-hidden="true" width="24" height="24" viewBox="0 0 24 24">
              <circle class="sun" cx="12" cy="12" r="6" fill="currentColor" />
              <g class="sun-beams" stroke="currentColor">
                  <line x1="12" y1="1" x2="12" y2="3" />
                  <line x1="12" y1="21" x2="12" y2="23" />
                  <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
                  <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
                  <line x1="1" y1="12" x2="3" y2="12" />
                  <line x1="21" y1="12" x2="23" y2="12" />
                  <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
                  <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
              </g>
              <path
                  class="moon"
                  fill="currentColor"
                  d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1 -8.313 -12.454z"
                  opacity="0"
              />
          </svg>
      </button>
  `

  const themeSwitcherStyles = `
      .theme-switcher {
          position: fixed;
          z-index: 1000;
          top: 1rem;
          right: 1rem;
          border: 0;
          border-radius: 50%;
          width: 40px;
          height: 40px;
          padding: 0;
          cursor: pointer;
          background: var(--primary);
          color: var(--white);
          transform-origin: center;
          transition: transform 0.1s ease;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
      }
      .theme-switcher:hover {
          transform: scale(1.1);
      }
      .theme-switcher:active {
          transform: scale(0.9);
      }
      .sun-and-moon {
          position: relative;
          width: 24px;
          height: 24px;
          transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
      }
      .sun {
          transform-origin: center;
          transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
      }
      .sun-beams {
          transform-origin: center;
          transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1),
                      opacity 0.5s cubic-bezier(0.4, 0, 0.2, 1);
      }
      .moon {
          transform-origin: center;
          transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1),
                      opacity 0.5s cubic-bezier(0.4, 0, 0.2, 1);
      }
      [data-theme="dark"] .sun-and-moon {
          transform: rotate(-180deg);
      }
      [data-theme="dark"] .sun {
          transform: scale(0);
      }
      [data-theme="dark"] .sun-beams {
          transform: rotate(45deg);
          opacity: 0;
      }
      [data-theme="dark"] .moon {
          transform: translateX(-2px);
          opacity: 1;
      }
      [data-theme="light"] .moon {
          transform: translateX(2px);
          opacity: 0;
      }
  `

  function addStyles(styles: string): void {
    const styleSheet = document.createElement('style')
    styleSheet.textContent = styles
    document.head.appendChild(styleSheet)
  }

  function addThemeSwitcher(): void {
    document.body.insertAdjacentHTML('beforeend', themeSwitcherHTML)
  }

  function updateImages(theme: string): void {
    const images = document.querySelectorAll('.lodge-info__logo') as NodeListOf<HTMLImageElement>
    images.forEach((img) => {
      const currentSrc = img.src
      if (theme === 'dark') {
        img.src = currentSrc.replace(/(\d+)\.png$/, 'dark_$1.png')
      } else {
        img.src = currentSrc.replace(/dark_(\d+)\.png$/, '$1.png')
      }
    })
  }

  function initializeTheme(): void {
    addStyles(themeSwitcherStyles)
    addThemeSwitcher()

    const savedTheme = localStorage.getItem('theme')
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    const defaultTheme = savedTheme || (prefersDark ? 'dark' : 'light')

    document.documentElement.setAttribute('data-theme', defaultTheme)
    updateImages(defaultTheme)

    const themeSwitcher = document.querySelector('.theme-switcher') as HTMLElement
    themeSwitcher.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme') as string
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark'

      document.documentElement.setAttribute('data-theme', newTheme)
      localStorage.setItem('theme', newTheme)
      updateImages(newTheme)
    })

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      if (!localStorage.getItem('theme')) {
        const newTheme = e.matches ? 'dark' : 'light'
        document.documentElement.setAttribute('data-theme', newTheme)
        updateImages(newTheme)
      }
    })
  }

  document.addEventListener('DOMContentLoaded', initializeTheme)

  const scrollTop = document.querySelector('.scroll-top') as HTMLElement

  if (scrollTop) {
    window.addEventListener('scroll', () => {
      if (window.pageYOffset > 200) {
        scrollTop.classList.add('visible')
      } else {
        scrollTop.classList.remove('visible')
      }
    })

    scrollTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    })
  }
}
