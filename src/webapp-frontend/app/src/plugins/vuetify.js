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
          primary: '#314439',
          secondary: '#F3B33C',
          accent: '#F38A00',
          background: '#FBF3EA',
          surface: '#bf5836',
        },
      },
      dark: {
        colors: {
          primary: '#344738',
          secondary: '#F7B232',
          accent: '#344738',
          background: '#16332D',
          surface: '#7B7653',
        },
      },
    },
  },
})
