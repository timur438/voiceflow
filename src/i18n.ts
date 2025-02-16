import { createI18n } from 'vue-i18n';

const messages = {
  en: {
    // General
    welcome: 'Welcome',
    language: 'Language',
    loading: 'Loading...',
    unexpectedError: 'Unexpected error, please try again',

    // Meetings
    myMeetings: 'My Meetings',
    addMeeting: 'Add Meeting',
    deleteMeeting: 'Delete Meeting',
    confirmDelete: 'Are you sure you want to delete this meeting?',
    deleteForever: 'The meeting "{{ meetingName }}" will be deleted forever. Without the possibility of recovery.',
    yes: 'Yes',
    cancel: 'Cancel',
    new: 'New',
    old: 'Old',
    uploaded: 'Uploaded',
    date: 'Date',
    name: 'Name',
    status: 'Status',
    length: 'Duration',
    source: 'Source',
    meetingName: 'Meeting name (optional)',
    meetingNamePlaceholder: 'Meeting name',

    // File Upload
    uploadFile: 'Upload audio or video file',
    chooseFile: 'Choose file',
    orDrag: 'or drag it here',
    anyFile: 'Any audio or video less than 1 GB',
    uploadMeeting: 'Upload Meeting',
    uploading: 'Uploading...',
    processing: 'Processing...',
    fileTooBig: 'File is too large. Maximum size is 1GB',
    selectFileAndName: 'Select a file and enter meeting name',
    uploadError: 'Upload error: {error}',
    serverError: 'Server error: {status} {statusText}',
    unknownError: 'Unknown error',

    // Auto-recording
    autoRecord: 'Auto-record meetings in calendar',
    recordAll: 'Record all my meetings in the calendar',
    doNotRecord: 'Do not record meetings automatically',

    // User Account
    apiKey: 'API Key',
    documentation: 'Documentation',
    copied: 'API key copied to clipboard',
    mySettings: 'My Settings',
    enterEmail: 'Enter your email',
    emailInfo: 'If the email is found in our database, a message will be sent to it.',
    send: 'Send',
    createPassword: 'Create your password',
    confirm: 'Confirm',
    login: 'Login',
    alreadyHaveAccount: 'Already have an account?',
    errorOccurred: 'An error occurred while sending the email',
    passwordComplexityInfo: 'The complexity of your password determines the level of protection for your account.',
    lostPasswordWarning: 'If you lose your password, your transcripts will be lost permanently.',
    password: 'Password',
    confirmPassword: 'Confirm Password',
    invalidCredentials: 'Invalid email or password',

    // Miscellaneous
    settingsAndIntegrations: 'Settings and Integrations',
    logout: 'Logout',
    back: 'Back',
    share: 'Share',
    export: 'Export',
    keywords: 'Keywords',
    participants: 'Participants',
    transcript: 'Transcript',
    summary: 'Summary'
  },
  ru: {
    // Общие
    welcome: 'Добро пожаловать',
    language: 'Язык',
    loading: 'Загрузка...',
    unexpectedError: 'Неожиданная ошибка, пожалуйста, попробуйте снова',

    // Встречи
    myMeetings: 'Мои встречи',
    addMeeting: 'Добавить встречу',
    deleteMeeting: 'Удалить встречу',
    confirmDelete: 'Вы точно хотите удалить встречу?',
    deleteForever: 'Встреча "{{ meetingName }}" будет удалена навсегда. Без возможности восстановления.',
    yes: 'Да',
    cancel: 'Отменить',
    new: 'Новая',
    old: 'Старая',
    uploaded: 'Загружено',
    date: 'Дата',
    name: 'Название',
    status: 'Статус',
    length: 'Длина',
    source: 'Источник',
    meetingName: 'Название встречи (опционально)',
    meetingNamePlaceholder: 'Название встречи',

    // Загрузка файлов
    uploadFile: 'Загрузка аудио или видео файла',
    chooseFile: 'Выберите файл',
    orDrag: 'или перетащите его сюда',
    anyFile: 'Любое аудио или видео меньше 1 ГБ',
    uploadMeeting: 'Загрузить встречу',
    uploading: 'Загрузка...',
    processing: 'Обработка...',
    fileTooBig: 'Файл слишком большой. Максимальный размер 1GB',
    selectFileAndName: 'Выберите файл и введите название встречи',
    uploadError: 'Ошибка при загрузке файла: {error}',
    serverError: 'Ошибка сервера: {status} {statusText}',
    unknownError: 'Неизвестная ошибка',

    // Автоматическая запись
    autoRecord: 'Авто-запись встреч в календаре',
    recordAll: 'Записывать все мои встречи в календаре',
    doNotRecord: 'Не записывать встречи автоматически',

    // Аккаунт пользователя
    apiKey: 'API Key',
    documentation: 'Документация',
    copied: 'API ключ скопирован в буфер обмена',
    mySettings: 'Мои настройки',
    enterEmail: 'Введите ваш email',
    emailInfo: 'Если почта найдется в нашей базе, на нее придет письмо.',
    send: 'Отправить',
    createPassword: 'Создайте пароль',
    confirm: 'Подтвердить',
    login: 'Вход',
    alreadyHaveAccount: 'Уже есть аккаунт?',
    errorOccurred: 'Произошла ошибка при отправке письма',
    passwordComplexityInfo: 'Сложность пароля определяет уровень защиты вашей учетной записи.',
    lostPasswordWarning: 'Если вы потеряете пароль, ваши транскрипты будут утеряны навсегда.',
    password: 'Пароль',
    confirmPassword: 'Повторите пароль',
    invalidCredentials: 'Неправильный логин или пароль',

    // Прочее
    settingsAndIntegrations: 'Настройки и интеграции',
    logout: 'Выйти',
    back: 'Назад',
    share: 'Поделиться',
    export: 'Экспорт',
    keywords: 'Ключевые слова',
    participants: 'Участники',
    transcript: 'Транскрипт',
    summary: 'Саммари'
  }
};

const i18n = createI18n({
  legacy: false,
  locale: 'ru',
  messages
});

export default i18n;