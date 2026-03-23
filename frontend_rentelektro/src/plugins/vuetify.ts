import '@mdi/font/css/materialdesignicons.css';
import 'vuetify/styles';
import { createVuetify, type ThemeDefinition } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

const rentElektroTheme: ThemeDefinition = {
  dark: false,
  colors: {
    background: '#f4f1ea',
    surface: '#fffdf8',
    primary: '#1f4d3a',
    secondary: '#cf6f2e',
    accent: '#7d8f69',
    success: '#2e7d32',
    warning: '#b7791f',
    error: '#c62828',
    info: '#1565c0',
  },
};

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'rentElektro',
    themes: {
      rentElektro: rentElektroTheme,
    },
  },
  defaults: {
    VApp: {
      style: 'background: linear-gradient(180deg, #f4f1ea 0%, #fbf8f1 45%, #f1ede5 100%);',
    },
    VAppBar: {
      elevation: 0,
      rounded: 'xl',
    },
    VBtn: {
      color: 'primary',
      rounded: 'lg',
      variant: 'flat',
      style: 'text-transform:none;font-weight:700;letter-spacing:-0.01em;',
    },
    VCard: {
      rounded: 'xl',
      class: 'app-surface-card',
    },
    VContainer: {
      class: 'app-max-width',
    },
    VSheet: {
      class: 'app-shell-card',
    },
    VTextField: {
      color: 'primary',
      density: 'comfortable',
      variant: 'outlined',
    },
    VTextarea: {
      color: 'primary',
      density: 'comfortable',
      variant: 'outlined',
    },
    VSelect: {
      color: 'primary',
      density: 'comfortable',
      variant: 'outlined',
    },
    VCheckbox: {
      color: 'primary',
      density: 'comfortable',
    },
    VAlert: {
      variant: 'tonal',
      rounded: 'lg',
    },
    VChip: {
      rounded: 'pill',
    },
  },
});

export default vuetify;
