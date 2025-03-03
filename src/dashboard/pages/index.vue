<template>
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-2xl font-bold mb-6">Weather Dashboard</h1>

        <!-- Add Location Button -->
        <div class="mb-4 flex justify-end">
            <UButton color="primary" @click="isAddLocationOpen = true"> Add Location </UButton>
        </div>

        <!-- Weather Table -->
        <UTable :columns="columns" :rows="locations" :loading="loading" @select="onSelectLocation">
            <template #loading>
                <div class="flex justify-center items-center p-4">
                    <UIcon name="i-heroicons-arrow-path" class="animate-spin mr-2" />
                    Loading weather data...
                </div>
            </template>

            <template #empty-state>
                <div class="flex flex-col items-center justify-center py-10">
                    <UIcon name="i-heroicons-cloud" class="text-4xl mb-2" />
                    <p class="text-gray-500">No locations added yet.</p>
                    <UButton color="primary" class="mt-4" @click="isAddLocationOpen = true">
                        Add your first location
                    </UButton>
                </div>
            </template>

            <template #condition-cell="{ row }">
                <div class="flex items-center">
                    <img
                        :src="`/icons/${getWeatherIcon(row.weather.wmo_code)}.svg`"
                        alt="Weather icon"
                        class="w-8 h-8 mr-2"
                    />
                </div>
            </template>

            <template #temperature-cell="{ row }">
                <span>{{ row.weather.temperature }}°C</span>
            </template>

            <template #rainfall-cell="{ row }">
                <span>{{ row.weather.rainfall }} mm</span>
            </template>

            <template #actions-cell="{ row }">
                <UButton color="red" variant="ghost" size="sm" @click.stop="confirmDelete(row)"> Remove </UButton>
            </template>
        </UTable>

        <!-- Add Location Modal -->
        <UModal v-model="isAddLocationOpen" :ui="{ width: 'sm:max-w-lg' }">
            <UCard>
                <template #header>
                    <div class="flex items-center justify-between">
                        <h3 class="text-xl font-semibold">Add Location</h3>
                        <UButton
                            icon="i-heroicons-x-mark"
                            color="gray"
                            variant="ghost"
                            @click="isAddLocationOpen = false"
                        />
                    </div>
                </template>

                <div class="py-4">
                    <UFormGroup label="Location" required>
                        <USelect
                            v-model="selectedLocation"
                            :options="filteredAvailableLocations"
                            option-attribute="name"
                            placeholder="Select a location"
                            :ui="{ padding: { base: 'p-3' } }"
                        />
                    </UFormGroup>
                </div>

                <template #footer>
                    <div class="flex justify-end gap-2">
                        <UButton color="gray" variant="ghost" @click="isAddLocationOpen = false"> Cancel </UButton>
                        <UButton color="primary" :disabled="!selectedLocation" @click="addNewLocation">
                            Add Location
                        </UButton>
                    </div>
                </template>
            </UCard>
        </UModal>

        <!-- Delete Confirmation Modal -->
        <UModal v-model="isDeleteConfirmOpen">
            <UCard>
                <template #header>
                    <div class="flex items-center justify-between">
                        <h3 class="text-xl font-semibold">Confirm Removal</h3>
                        <UButton
                            icon="i-heroicons-x-mark"
                            color="gray"
                            variant="ghost"
                            @click="isDeleteConfirmOpen = false"
                        />
                    </div>
                </template>

                <div class="py-4">
                    <p>
                        Are you sure you want to remove <strong>{{ locationToDelete?.name }}</strong> from your
                        dashboard?
                    </p>
                </div>

                <template #footer>
                    <div class="flex justify-end gap-2">
                        <UButton color="gray" variant="ghost" @click="isDeleteConfirmOpen = false"> Cancel </UButton>
                        <UButton color="red" @click="deleteConfirmed"> Remove </UButton>
                    </div>
                </template>
            </UCard>
        </UModal>

        <!-- Forecast Sidebar -->
        <USlideover v-model="isForecastOpen" :ui="{ width: 'w-full max-w-md' }">
            <UCard v-if="forecast" class="h-full">
                <template #header>
                    <div class="flex items-center justify-between">
                        <h3 class="text-xl font-semibold">{{ forecast.location_name }} Forecast</h3>
                        <UButton
                            icon="i-heroicons-x-mark"
                            color="gray"
                            variant="ghost"
                            @click="isForecastOpen = false"
                        />
                    </div>
                </template>

                <div class="py-4 overflow-auto">
                    <div v-for="day in forecast.days" :key="day.date" class="mb-6 border-b pb-4 last:border-b-0">
                        <div class="flex items-center justify-between mb-2">
                            <h4 class="font-medium text-lg">{{ formatDate(day.date) }}</h4>
                            <img
                                :src="`/icons/${getWeatherIcon(day.wmo_code)}.svg`"
                                alt="Weather icon"
                                class="w-8 h-8"
                            />
                        </div>
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <p class="text-sm text-gray-500">Temperature</p>
                                <p class="text-lg font-semibold">{{ day.temperature }}°C</p>
                            </div>
                            <div>
                                <p class="text-sm text-gray-500">Rainfall</p>
                                <p class="text-lg font-semibold">{{ day.rainfall }} mm</p>
                            </div>
                        </div>
                    </div>
                </div>
            </UCard>
            <div v-else class="flex justify-center items-center h-full">
                <UIcon name="i-heroicons-arrow-path" class="animate-spin mr-2" />
                Loading forecast data...
            </div>
        </USlideover>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { getWeatherIcon, formatDate } from '../pages/utils/weather';

const { getLocations, addLocation, deleteLocation, getForecast } = useApi();

// Table configuration
const columns = [
    { key: 'condition', label: 'Condition' },
    { key: 'name', label: 'Location' },
    { key: 'temperature', label: 'Temperature' },
    { key: 'rainfall', label: 'Rainfall' },
    { key: 'actions', label: '' },
];

// State
const loading = ref(true);
const locations = ref([]);
const isAddLocationOpen = ref(false);
const isDeleteConfirmOpen = ref(false);
const isForecastOpen = ref(false);
const locationToDelete = ref(null);
const selectedLocation = ref(null);
const forecast = ref(null);

// Available locations from the GitHub gist
const availableLocations = ref([
    { id: 1, name: 'Berlin', latitude: 52.52, longitude: 13.41 },
    { id: 2, name: 'London', latitude: 51.51, longitude: -0.13 },
    { id: 3, name: 'New York', latitude: 40.71, longitude: -74.01 },
    { id: 4, name: 'Paris', latitude: 48.85, longitude: 2.35 },
    { id: 5, name: 'Tokyo', latitude: 35.69, longitude: 139.69 },
    { id: 6, name: 'Sydney', latitude: -33.87, longitude: 151.21 },
    { id: 7, name: 'Rio de Janeiro', latitude: -22.91, longitude: -43.17 },
    { id: 8, name: 'Cairo', latitude: 30.05, longitude: 31.25 },
    { id: 9, name: 'Moscow', latitude: 55.75, longitude: 37.62 },
    { id: 10, name: 'Los Angeles', latitude: 34.05, longitude: -118.24 },
]);

// Filter available locations to only show those that haven't been added yet
const filteredAvailableLocations = computed(() => {
    const existingNames = locations.value.map((loc) => loc.name);
    return availableLocations.value.filter((loc) => !existingNames.includes(loc.name));
});

// Fetch locations on mount
onMounted(async () => {
    await fetchLocations();
});

// Methods
const fetchLocations = async () => {
    loading.value = true;
    try {
        locations.value = await getLocations();
    } catch (error) {
        console.error('Error fetching locations:', error);
    } finally {
        loading.value = false;
    }
};

const addNewLocation = async () => {
    if (!selectedLocation.value) return;

    try {
        await addLocation({
            name: selectedLocation.value.name,
            latitude: selectedLocation.value.latitude,
            longitude: selectedLocation.value.longitude,
        });

        // Refresh locations
        await fetchLocations();

        // Reset and close modal
        selectedLocation.value = null;
        isAddLocationOpen.value = false;
    } catch (error) {
        console.error('Error adding location:', error);
    }
};

const confirmDelete = (location) => {
    locationToDelete.value = location;
    isDeleteConfirmOpen.value = true;
};

const deleteConfirmed = async () => {
    if (!locationToDelete.value) return;

    try {
        await deleteLocation(locationToDelete.value.id);

        // Refresh locations
        await fetchLocations();

        // Close modal and reset
        isDeleteConfirmOpen.value = false;
        locationToDelete.value = null;
    } catch (error) {
        console.error('Error deleting location:', error);
    }
};

const onSelectLocation = async (location) => {
    try {
        forecast.value = null;
        isForecastOpen.value = true;
        forecast.value = await getForecast(location.id);
    } catch (error) {
        console.error('Error fetching forecast:', error);
    }
};
</script>
