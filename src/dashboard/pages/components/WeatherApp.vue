<template>
    <div class="weather-app bg-gray-900 min-h-screen text-white">
        <div class="container mx-auto px-4 py-8">
            <header class="flex justify-between items-center mb-6">
                <h1 class="text-2xl font-bold flex items-center">
                    <WeatherIcon :wmo-code="0" class="w-8 h-8 mr-2" />
                    Weather App
                </h1>
                <div class="text-gray-300">{{ currentLocation }}</div>
            </header>

            <!-- Error Message -->
            <div v-if="errorMessage" class="bg-red-600 text-white p-4 rounded mb-4">
                {{ errorMessage }}
                <button @click="errorMessage = ''" class="float-right hover:text-gray-200">&times;</button>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- Locations List -->
                <div class="bg-gray-800 rounded-lg p-4">
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="text-xl font-semibold">Locations</h2>
                        <button
                            @click="openAddLocationModal"
                            class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded"
                        >
                            + Add Location
                        </button>
                    </div>

                    <table class="w-full">
                        <thead class="text-gray-400">
                            <tr>
                                <th class="text-left">Location</th>
                                <th class="text-right">Temperature</th>
                                <th class="text-right">Rainfall</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="location in locations"
                                :key="location.id"
                                @click="selectLocation(location)"
                                class="cursor-pointer hover:bg-gray-700 transition"
                                :class="{ 'bg-gray-700': selectedLocation?.id === location.id }"
                            >
                                <td class="flex items-center py-2">
                                    <WeatherIcon :wmo-code="location.weather.wmo_code" class="mr-2 w-6 h-6" />
                                    {{ location.name }}
                                </td>
                                <td class="text-right">{{ location.weather.temperature }}°C</td>
                                <td class="text-right">{{ location.weather.rainfall }} mm</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Location Details -->
                <div v-if="selectedLocation" class="bg-gray-800 rounded-lg p-4 col-span-2">
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="text-xl font-semibold">{{ selectedLocation.name }}</h2>
                        <button @click="closeLocationDetails" class="text-gray-400 hover:text-white text-2xl">
                            &times;
                        </button>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <!-- Current Weather -->
                        <div>
                            <div class="text-6xl font-bold">{{ selectedLocation.weather.temperature }}°C</div>
                            <div class="mt-2 text-gray-400">
                                {{ getWeatherDescription(selectedLocation.weather.wmo_code) }}
                            </div>
                        </div>

                        <!-- Weekly Forecast -->
                        <div>
                            <h3 class="text-lg font-semibold mb-4">This Week</h3>
                            <div class="space-y-2">
                                <div
                                    v-for="day in weeklyForecast"
                                    :key="day.day"
                                    class="flex justify-between items-center bg-gray-700 p-2 rounded"
                                >
                                    <div class="flex items-center">
                                        <WeatherIcon :wmo-code="day.wmoCode" class="mr-2 w-6 h-6" />
                                        {{ day.day }}
                                    </div>
                                    <div class="text-right">Min {{ day.min }}°C / Max {{ day.max }}°C</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Add Location Modal -->
            <div
                v-if="showAddLocationModal"
                class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
            >
                <div class="bg-gray-800 p-6 rounded-lg w-96 relative">
                    <button
                        @click="closeAddLocationModal"
                        class="absolute top-2 right-2 text-gray-400 hover:text-white text-2xl"
                    >
                        &times;
                    </button>
                    <h2 class="text-xl font-semibold mb-4">Add Location</h2>
                    <input
                        v-model="newLocationInput"
                        placeholder="Enter city name"
                        class="w-full p-2 mb-4 bg-gray-700 rounded"
                        @keyup.enter="addLocation"
                    />
                    <button
                        @click="addLocation"
                        class="w-full bg-blue-500 text-white py-2 rounded"
                        :disabled="!newLocationInput.trim()"
                    >
                        Add Location
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import WeatherIcon from './WeatherIcon.vue';
import { useWeatherAPI } from '~/composables/useWeatherAPI';

// Use the useWeatherAPI composable
const { fetchLocations, addLocation: apiAddLocation } = useWeatherAPI();

const locations = ref([]);
const selectedLocation = ref(null);
const showAddLocationModal = ref(false);
const newLocationInput = ref('');
const currentLocation = ref('New York, US');
const errorMessage = ref('');
const weeklyForecast = ref([
    { day: 'Sunday', min: 16, max: 20, wmoCode: 2 },
    { day: 'Monday', min: 12, max: 22, wmoCode: 3 },
    { day: 'Tuesday', min: 13, max: 21, wmoCode: 1 },
    { day: 'Wednesday', min: 18, max: 25, wmoCode: 0 },
    { day: 'Thursday', min: 16, max: 20, wmoCode: 3 },
    { day: 'Friday', min: 14, max: 23, wmoCode: 0 },
    { day: 'Saturday', min: 12, max: 24, wmoCode: 3 },
]);

const fetchLocationsData = async () => {
    try {
        locations.value = await fetchLocations();

        // Auto-select first location if exists
        if (locations.value.length > 0) {
            selectedLocation.value = locations.value[0];
        }
    } catch (error) {
        console.error('Failed to fetch locations:', error);
        errorMessage.value = 'Unable to fetch locations. Please check your connection.';
    }
};

onMounted(fetchLocationsData);

const selectLocation = (location) => {
    selectedLocation.value = location;
};

const closeLocationDetails = () => {
    selectedLocation.value = null;
};

const openAddLocationModal = () => {
    showAddLocationModal.value = true;
    newLocationInput.value = '';
};

const closeAddLocationModal = () => {
    showAddLocationModal.value = false;
    newLocationInput.value = '';
};

const addLocation = async () => {
    const locationName = newLocationInput.value.trim();
    if (!locationName) return;

    try {
        const newLocation = await apiAddLocation({
            name: locationName,
            latitude: 0, // Mock values - backend should handle this
            longitude: 0,
        });

        // Add new location to the list
        locations.value.push(newLocation);

        // Select the newly added location
        selectedLocation.value = newLocation;

        // Close the modal
        closeAddLocationModal();
    } catch (error) {
        console.error('Failed to add location:', error);
        errorMessage.value = 'Unable to add location. Please try again.';
    }
};

const getWeatherDescription = (wmoCode) => {
    const descriptions = {
        0: 'Clear Sky',
        1: 'Mainly Clear',
        2: 'Partly Cloudy',
        3: 'Overcast',
    };
    return descriptions[wmoCode] || 'Unknown';
};
</script>
