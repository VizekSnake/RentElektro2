<template>
  <footer class="app-footer">
    <v-container class="app-footer-shell">
      <div class="app-footer-grid">
        <div class="d-flex flex-column ga-3">
          <div class="text-overline">RentElektro</div>
          <div class="text-h6 font-weight-bold">
            Marketplace do wynajmu narzędzi w nowoczesnej formie.
          </div>
          <p class="app-muted-copy mb-0">
            Katalog ofert, profile użytkowników i prosty przepływ wynajmu.
          </p>
        </div>

        <div class="d-flex flex-column ga-3">
          <div class="text-overline">Nawigacja</div>
          <div class="d-flex flex-column ga-2">
            <router-link to="/home" class="app-footer-link">Strona główna</router-link>
            <router-link to="/tools" class="app-footer-link">Narzędzia</router-link>
            <router-link to="/about" class="app-footer-link">O serwisie</router-link>
            <router-link to="/rentals" class="app-footer-link">Centrum wynajmów</router-link>
          </div>
        </div>

        <div class="d-flex flex-column ga-3">
          <div class="text-overline">Akcje</div>
          <div class="d-flex flex-column ga-2">
            <router-link to="/signup" class="app-footer-link">Załóż konto</router-link>
            <router-link to="/login" class="app-footer-link">Zaloguj się</router-link>
            <router-link to="/tool/add" class="app-footer-link">Dodaj ofertę</router-link>
          </div>
        </div>
      </div>

      <div class="app-footer-bottom">
        <span>© 2026 RentElektro</span>
        <span>FastAPI · Vue · Vuetify</span>
      </div>
    </v-container>
  </footer>
</template>
