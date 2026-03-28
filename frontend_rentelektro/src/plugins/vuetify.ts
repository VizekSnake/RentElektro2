import '@mdi/font/css/materialdesignicons.css';
import 'vuetify/styles';
import { createVuetify, type ThemeDefinition } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

const rentElektroTheme: ThemeDefinition = {
  dark: false,
  colors: {
    background: '#f7f4ef',
    surface: '#ffffff',
    primary: '#f97316',
    secondary: '#1f2937',
    accent: '#fdba74',
    success: '#2e7d32',
    warning: '#d97706',
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
      style: 'background: linear-gradient(180deg, #fbf9f5 0%, #f6f1e8 42%, #f3ece1 100%);',
    },
    VAppBar: {
      elevation: 0,
      rounded: 'xl',
    },
    VBtn: {
      color: 'primary',
      rounded: 'xl',
      variant: 'flat',
      style: 'text-transform:none;font-weight:700;letter-spacing:-0.02em;',
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
      rounded: 'xl',
    },
    VTextarea: {
      color: 'primary',
      density: 'comfortable',
      variant: 'outlined',
      rounded: 'xl',
    },
    VSelect: {
      color: 'primary',
      density: 'comfortable',
      variant: 'outlined',
      rounded: 'xl',
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
