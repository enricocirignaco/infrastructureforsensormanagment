// src/plugins/vuetify.js
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import '@mdi/font/css/materialdesignicons.css'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'dark',
    themes: {
      light: {
        colors: {
          primary: '#4A6D48',
          secondary: '#E3A427',
          accent: '#5C8B5C',
          background: '#FFFFFF',
          surface: '#D9D1A0',
        },
      },
      dark: {
        colors: {
          primary: '#344738',
          secondary: '#F7B232',
          accent: '#344738',
          background: '#16332D',
          surface: '#7B7653',
          error: '#F02222',
          info: '#FFFFFF',
        },
      },
    },
  },
})
