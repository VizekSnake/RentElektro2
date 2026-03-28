<template>
  <v-container class="app-tool-list-page">
    <section class="app-tool-list-hero">
      <div class="app-home-kicker">
        <v-icon size="18">mdi-view-grid-plus-outline</v-icon>
        Katalog ofert
      </div>

      <div class="d-flex flex-column flex-lg-row justify-space-between align-lg-end ga-5 mt-4">
        <div>
          <h1 class="app-product-title ma-0">Narzędzia gotowe do wynajmu.</h1>
          <p class="app-product-copy mt-3 mb-0">
            Przeglądaj oferty w nowym katalogu, filtruj po zasilaniu, dostępności i kategorii, a potem przechodź do szczegółów konkretnego sprzętu.
          </p>
        </div>

        <div class="d-flex flex-wrap ga-3">
          <AppButton to="/tool/add" size="large" prepend-icon="mdi-plus-circle-outline">
            Dodaj narzędzie
          </AppButton>
        </div>
      </div>

      <div class="app-tool-list-stat-row">
        <div class="app-product-stat-card">
          <div class="app-product-stat-label">Łącznie ofert</div>
          <div class="app-product-stat-value">{{ total }}</div>
        </div>
        <div class="app-product-stat-card">
          <div class="app-product-stat-label">Strona</div>
          <div class="app-product-stat-value">{{ page }}/{{ totalPages }}</div>
        </div>
        <div class="app-product-stat-card">
          <div class="app-product-stat-label">Na stronie</div>
          <div class="app-product-stat-value">{{ tools.length }}</div>
        </div>
      </div>
    </section>

    <section class="app-tool-list-filters">
      <div class="app-tool-list-filter-card">
        <div class="d-flex flex-column flex-lg-row justify-space-between ga-4 mb-5">
          <div>
            <div class="text-overline mb-2">Filtry</div>
            <h2 class="text-h5 font-weight-bold mb-2">Zawęź katalog</h2>
            <p class="app-muted-copy mb-0">
              Zmiana filtrów odświeża listę z backendu, więc nie ciągniemy całej bazy narzędzi na frontend.
            </p>
          </div>
          <div class="d-flex align-start">
            <AppButton variant="outlined" color="secondary" prepend-icon="mdi-filter-off-outline" @click="resetFilters">
              Wyczyść filtry
            </AppButton>
          </div>
        </div>

        <v-row>
          <v-col cols="12" md="6" lg="4">
            <AppTextField
              v-model="filters.search"
              label="Szukaj"
              prepend-inner-icon="mdi-magnify"
              placeholder="Typ, marka lub opis"
              @update:model-value="handleFilterChange"
            />
          </v-col>
          <v-col cols="12" md="6" lg="2">
            <AppSelect
              v-model="filters.power_source"
              label="Zasilanie"
              :items="powerSourceOptions"
              item-title="title"
              item-value="value"
              clearable
              @update:model-value="handleFilterChange"
            />
          </v-col>
          <v-col cols="12" md="6" lg="2">
            <AppSelect
              v-model="filters.availability"
              label="Dostępność"
              :items="availabilityOptions"
              item-title="title"
              item-value="value"
              clearable
              @update:model-value="handleFilterChange"
            />
          </v-col>
          <v-col cols="12" md="6" lg="2">
            <AppSelect
              v-model="filters.category_id"
              label="Kategoria"
              :items="categoryOptions"
              item-title="title"
              item-value="value"
              clearable
              @update:model-value="handleFilterChange"
            />
          </v-col>
          <v-col cols="12" md="6" lg="2">
            <AppSelect
              v-model="filters.sort"
              label="Sortowanie"
              :items="sortOptions"
              item-title="title"
              item-value="value"
              @update:model-value="handleFilterChange"
            />
          </v-col>
        </v-row>
      </div>
    </section>

    <ResponseMessage v-if="errorMessage" :message="errorMessage" type="error" />

    <CardGridSkeleton v-if="isLoading" />

    <EmptyState
      v-else-if="tools.length === 0"
      title="Brak wyników"
      subtitle="Nie znaleziono ofert spełniających wybrane kryteria. Zmień filtry albo dodaj nowe narzędzie."
    >
      <template #actions>
        <AppButton to="/tool/add" prepend-icon="mdi-hammer-wrench">
          Dodaj pierwsze narzędzie
        </AppButton>
      </template>
    </EmptyState>

    <template v-else>
      <section class="app-tool-list-grid">
        <v-row>
          <v-col v-for="tool in tools" :key="tool.id" cols="12" md="6" xl="4">
            <ToolCard :tool="tool" />
          </v-col>
        </v-row>
      </section>

      <section class="app-tool-list-pagination">
        <div class="app-tool-list-pagination-card">
          <div class="app-muted-copy">Strona {{ page }} z {{ totalPages }}</div>
          <v-pagination
            :model-value="page"
            :length="totalPages"
            :total-visible="6"
            active-color="primary"
            @update:model-value="handlePageChange"
          />
        </div>
      </section>
    </template>
  </v-container>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive } from 'vue';
import { useToolList } from '@/composables/useToolList';
import { fetchToolCategories } from '@/services/toolService';
import AppButton from '@/shared/ui/atoms/AppButton.vue';
import AppSelect from '@/shared/ui/atoms/AppSelect.vue';
import AppTextField from '@/shared/ui/atoms/AppTextField.vue';
import CardGridSkeleton from '@/shared/ui/organisms/CardGridSkeleton.vue';
import EmptyState from '@/shared/ui/organisms/EmptyState.vue';
import ResponseMessage from '@/shared/ui/molecules/ResponseMessage.vue';
import ToolCard from '@/features/tools/components/ToolCard.vue';
import { createLogger } from '@/shared/lib/logger';
import type { ToolCategory, ToolListFilters } from '@/types/tools';

const logger = createLogger('tool-list-view');
const { tools, isLoading, errorMessage, total, totalPages, page, fetchTools: loadTools } = useToolList();
const categories = reactive<ToolCategory[]>([]);
const filters = reactive<ToolListFilters>({
  search: '',
  power_source: undefined,
  availability: undefined,
  category_id: undefined,
  sort: 'newest',
  page: 1,
  page_size: 9,
});

const sortOptions = [
  { title: 'Najnowsze', value: 'newest' },
  { title: 'Cena rosnąco', value: 'price_asc' },
  { title: 'Cena malejąco', value: 'price_desc' },
  { title: 'Nazwa A-Z', value: 'name' },
];

const powerSourceOptions = [
  { title: 'Elektryczne', value: 'electric' },
  { title: 'Spalinowe', value: 'gas' },
];

const availabilityOptions = [
  { title: 'Dostępne', value: true },
];

const categoryOptions = computed(() =>
  categories.map((category) => ({
    title: category.name,
    value: category.id,
  })),
);

const currentFilters = (): ToolListFilters => ({
  search: filters.search?.trim() || undefined,
  power_source: filters.power_source,
  availability: filters.availability,
  category_id: filters.category_id,
  sort: filters.sort,
  page: filters.page,
  page_size: filters.page_size,
});

const fetchTools = async (): Promise<void> => {
  const previousError = errorMessage.value;
  await loadTools(currentFilters());
  if (errorMessage.value && errorMessage.value !== previousError) {
    logger.error('fetch_tools_failed', errorMessage.value);
  }
};

const fetchCategories = async (): Promise<void> => {
  try {
    const result = await fetchToolCategories();
    categories.splice(0, categories.length, ...result.filter((item) => item.active));
  } catch (error) {
    logger.error('fetch_categories_failed', error);
  }
};

const handleFilterChange = (): void => {
  filters.page = 1;
  void fetchTools();
};

const handlePageChange = (value: number): void => {
  filters.page = value;
  void fetchTools();
};

const resetFilters = (): void => {
  filters.search = '';
  filters.power_source = undefined;
  filters.availability = undefined;
  filters.category_id = undefined;
  filters.sort = 'newest';
  filters.page = 1;
  void fetchTools();
};

onMounted(() => {
  void fetchCategories();
  void fetchTools();
});
</script>
