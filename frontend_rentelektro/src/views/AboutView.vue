<template>
  <div class="app-about">
    <v-container class="app-max-width">
      <section class="app-about-hero">
        <div class="app-about-hero-grid">
          <div class="d-flex flex-column ga-6">
            <div class="d-flex flex-column ga-4">
              <div class="app-home-kicker">O serwisie</div>
              <h1 class="app-home-title mb-0">Wynajem narzędzi, który naprawdę oszczędza czas.</h1>
              <p class="app-home-copy mb-0">
                RentElektro łączy osoby, które potrzebują sprawdzonego sprzętu na chwilę, z właścicielami
                narzędzi gotowymi udostępnić go lokalnie. Bez dzwonienia po znajomych, bez przypadkowych
                ogłoszeń i bez zgadywania, czy ktoś w ogóle odpisze.
              </p>
            </div>

            <div class="app-home-stat-grid">
              <div class="app-home-glass-card">
                <div class="app-home-stat-value">24h</div>
                <div class="app-home-stat-label">Szybka ścieżka od znalezienia sprzętu do wysłania prośby</div>
              </div>
              <div class="app-home-glass-card">
                <div class="app-home-stat-value">Lokalnie</div>
                <div class="app-home-stat-label">Oferty od osób i firm działających w Twojej okolicy</div>
              </div>
              <div class="app-home-glass-card">
                <div class="app-home-stat-value">Czytelnie</div>
                <div class="app-home-stat-label">Jasne stawki, terminy, komentarze i decyzje właściciela</div>
              </div>
            </div>
          </div>

          <div class="app-about-showcase">
            <div class="app-about-showcase-card">
              <div class="text-overline text-white text-opacity-70 mb-3">Jak to działa</div>
              <div class="d-flex flex-column ga-3">
                <div class="app-about-step">
                  <span>1</span>
                  <div>
                    <strong>Wybierasz narzędzie</strong>
                    <div>Przeglądasz ofertę, zdjęcia, stawkę i dostępność.</div>
                  </div>
                </div>
                <div class="app-about-step">
                  <span>2</span>
                  <div>
                    <strong>Wysyłasz prośbę</strong>
                    <div>Podajesz termin i od razu dopisujesz krótki komentarz.</div>
                  </div>
                </div>
                <div class="app-about-step">
                  <span>3</span>
                  <div>
                    <strong>Otrzymujesz decyzję</strong>
                    <div>Właściciel akceptuje lub odrzuca zgłoszenie z własną wiadomością.</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="app-home-section">
        <div class="app-home-bento">
          <article class="app-home-bento-card">
            <div class="text-overline mb-2">Dla osób prywatnych</div>
            <h2 class="text-h5 font-weight-bold mb-3">Nie kupuj sprzętu, którego użyjesz dwa razy.</h2>
            <p class="app-muted-copy mb-0">
              Wiertarka na weekendowy remont, myjka do ogrodu, piła do jednej realizacji. RentElektro
              pozwala wypożyczyć dokładnie to, czego potrzebujesz, tylko na czas, kiedy faktycznie z tego korzystasz.
            </p>
          </article>

          <article class="app-home-bento-card app-home-bento-dark">
            <div class="text-overline mb-2 text-white text-opacity-70">Dla właścicieli</div>
            <h2 class="text-h5 font-weight-bold mb-3">Zamień nieużywany sprzęt w regularny przychód.</h2>
            <p class="text-body-1 text-white text-opacity-70 mb-0">
              Dodajesz narzędzie, ustawiasz stawkę i decydujesz, komu je udostępnić. Wszystkie prośby
              i komentarze zbierają się w jednym miejscu, więc łatwo pilnować całego procesu.
            </p>
          </article>
        </div>
      </section>

      <section class="app-home-section">
        <div class="app-section-header mb-8">
          <div class="text-overline mb-2">Dlaczego RentElektro</div>
          <h2 class="text-h4 font-weight-bold mb-3">Serwis zaprojektowany pod realne wypożyczenia.</h2>
          <p class="app-muted-copy mb-0">
            Zamiast anonimowych ogłoszeń masz czytelny proces, widoczny status zgłoszenia i prosty kontakt
            między stronami.
          </p>
        </div>

        <v-row>
          <v-col cols="12" md="4">
            <article class="app-home-feature-card">
              <div class="app-home-feature-icon mb-4">
                <v-icon size="26">mdi-map-marker-radius-outline</v-icon>
              </div>
              <h3 class="text-h6 font-weight-bold mb-2">Lokalny charakter</h3>
              <p class="app-muted-copy mb-0">
                Sprzęt jest bliżej niż w dużych, bezosobowych wypożyczalniach. To wygodniejsze dla obu stron.
              </p>
            </article>
          </v-col>
          <v-col cols="12" md="4">
            <article class="app-home-feature-card">
              <div class="app-home-feature-icon mb-4">
                <v-icon size="26">mdi-message-text-outline</v-icon>
              </div>
              <h3 class="text-h6 font-weight-bold mb-2">Jasna komunikacja</h3>
              <p class="app-muted-copy mb-0">
                Komentarz najemcy, odpowiedź właściciela i status zgłoszenia są widoczne bez szukania po wiadomościach.
              </p>
            </article>
          </v-col>
          <v-col cols="12" md="4">
            <article class="app-home-feature-card">
              <div class="app-home-feature-icon mb-4">
                <v-icon size="26">mdi-shield-check-outline</v-icon>
              </div>
              <h3 class="text-h6 font-weight-bold mb-2">Większa kontrola</h3>
              <p class="app-muted-copy mb-0">
                Właściciel sam podejmuje decyzję, a użytkownik dokładnie widzi, na jakim etapie jest prośba.
              </p>
            </article>
          </v-col>
        </v-row>
      </section>

      <section class="app-home-section">
        <div class="app-home-cta">
          <div class="d-flex flex-column flex-md-row justify-space-between align-md-center ga-4">
            <div>
              <div class="text-overline text-white text-opacity-70 mb-2">Gotowy, żeby zacząć?</div>
              <h2 class="text-h4 font-weight-bold mb-2">Znajdź sprzęt na najbliższy projekt albo wystaw własne narzędzia.</h2>
              <p class="text-body-1 text-white text-opacity-80 mb-0">
                RentElektro upraszcza wypożyczenia od pierwszego kliknięcia aż po decyzję właściciela.
              </p>
            </div>
            <div class="d-flex flex-wrap ga-3">
              <AppButton color="white" to="/tools">Przeglądaj narzędzia</AppButton>
              <AppButton color="secondary" variant="outlined" to="/signup">Załóż konto</AppButton>
            </div>
          </div>
        </div>
      </section>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import AppButton from '@/shared/ui/atoms/AppButton.vue';
</script>
