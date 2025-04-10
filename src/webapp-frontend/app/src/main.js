    import { createApp } from 'vue'
    import { createPinia } from 'pinia'

    import App from './App.vue'
    import router from './router'
    // Import the Vuetify plugin configuration
    import vuetify from './plugins/vuetify'

    const app = createApp(App)

    app.use(vuetify)
    app.use(createPinia())
    app.use(router)

    app.mount('#app')
