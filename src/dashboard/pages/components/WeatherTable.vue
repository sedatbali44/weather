<!-- frontend/components/weather/WeatherTable.vue -->
<template>
    <div class="weather-table-container">
        <div class="header-actions mb-4">
            <UButton icon="i-heroicons-plus" color="primary" @click="openAddLocationModal"> Add Location </UButton>
        </div>

        <UTable
            :columns="columns"
            :rows="locations"
            :loading="loading"
            :empty-state="{ icon: 'i-heroicons-cloud', label: 'No locations added yet' }"
            @click:row="openLocationDetails"
        >
            <template #icon-data="{ row }">
                <img :src="`/icons/${getWeatherIcon(row.current.weather_code)}`" alt="Weather icon" class="w-8 h-8" />
            </template>

            <template #temperature-data="{ row }"> {{ row.current.temperature }}°C </template>

            <template #rainfall-data="{ row }"> {{ row.current.rainfall }} mm </template>

            <template #actions-data="{ row }">
                <UButton
                    icon="i-heroicons-trash"
                    color="red"
                    variant="ghost"
                    @click.stop="openDeleteConfirmation(row)"
                />
            </template>
        </UTable>

        <!-- Add Location Modal -->
        <AddLocationModal v-model:open="isAddLocationModalOpen" @location-added="fetchLocationsData" />

        <!-- Delete Confirmation Modal -->
        <ConfirmationModal
            v-model:open="isConfirmationModalOpen"
            :title="`Remove ${locationToDelete?.name}?`"
            :message="`Are you sure you want to remove ${locationToDelete?.name} from your locations?`"
            @confirm="deleteLocation"
        />

        <!-- Weather Details Sidebar -->
        <WeatherDetails v-model:open="isDetailsSidebarOpen" :location-id="selectedLocationId" />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getWeatherIcon } from '../utils/wmoCodeToIcon';
import AddLocationModal from './AddLocationModal.vue';
import ConfirmationModal from './ConfirmationModal.vue';
import WeatherDetails from './WeatherDetails.vue';

const isAddLocationModalOpen = ref(false);
const isConfirmationModalOpen = ref(false);
const isDetailsSidebarOpen = ref(false);
const selectedLocationId = ref(null);
const locationToDelete = ref(null);
const locations = ref([]);
const loading = ref(true);

const { fetchLocations, removeLocation } = useWeatherAPI();

const columns = [
    {
        key: 'icon',
        label: '',
    },
    {
        key: 'name',
        label: 'Location',
    },
    {
        key: 'temperature',
        label: 'Temperature',
    },
    {
        key: 'rainfall',
        label: 'Rainfall',
    },
    {
        key: 'actions',
        label: '',
    },
];

const fetchLocationsData = async () => {
    loading.value = true;
    locations.value = await fetchLocations();
    loading.value = false;
};

const openAddLocationModal = () => {
    isAddLocationModalOpen.value = true;
};

const openDeleteConfirmation = (location) => {
    locationToDelete.value = location;
    isConfirmationModalOpen.value = true;
};

const deleteLocation = async () => {
    if (locationToDelete.value) {
        await removeLocation(locationToDelete.value.id);
        await fetchLocationsData();
        isConfirmationModalOpen.value = false;
    }
};

const openLocationDetails = (row) => {
    selectedLocationId.value = row.id;
    isDetailsSidebarOpen.value = true;
};

onMounted(fetchLocationsData);
</script>
