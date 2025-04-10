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
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#F08700',
          secondary: '#AA5302',
          accent: '#F5C879',
          background: '#FEFEFE',
          surface: '#FDF6EB',
        }
      },
      dark: {
        colors: {
          primary: '#030100',
          secondary: '#7B7653',
          accent: '#344738',
          background: '#F7B232',
          surface: '#16332D',
        }
      }
    },
  },
})