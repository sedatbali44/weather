<!-- frontend/components/weather/WeatherDetails.vue -->
<template>
    <USlideover v-model="isOpen" :ui="{ width: 'sm:max-w-lg' }">
        <UCard>
            <template #header>
                <div class="flex items-center justify-between">
                    <h3 class="text-lg font-semibold">{{ forecast?.location_name || 'Weather Forecast' }}</h3>
                    <UButton icon="i-heroicons-x-mark" color="gray" variant="ghost" @click="closeSidebar" />
                </div>
            </template>

            <div>
                <div v-if="loading" class="py-8 text-center">
                    <UIcon name="i-heroicons-arrow-path" class="animate-spin h-8 w-8 mx-auto text-gray-400" />
                    <p class="mt-2 text-gray-500">Loading forecast...</p>
                </div>

                <div v-else-if="!forecast" class="py-8 text-center text-gray-500">Failed to load forecast data</div>

                <div v-else class="space-y-4 py-2">
                    <div v-for="(day, index) in forecast.daily" :key="index" class="border-b last:border-0 pb-4">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2">
                                <img
                                    :src="`/icons/${getWeatherIcon(day.weather_code)}`"
                                    alt="Weather icon"
                                    class="w-8 h-8"
                                />
                                <div>
                                    <p class="font-medium">{{ formatDate(day.date) }}</p>
                                    <p class="text-sm text-gray-500">{{ getWeatherDescription(day.weather_code) }}</p>
                                </div>
                            </div>

                            <div class="text-right">
                                <p>
                                    <span class="font-medium">{{ day.temperature_max.toFixed(1) }}°</span>
                                    <span class="text-gray-500">{{ day.temperature_min.toFixed(1) }}°</span>
                                </p>
                                <p class="text-sm text-gray-500">{{ day.rainfall_sum.toFixed(1) }} mm</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </UCard>
    </USlideover>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { getWeatherIcon } from '../utils/wmoCodeToIcon';

const props = defineProps({
    open: {
        type: Boolean,
        default: false,
    },
    locationId: {
        type: Number,
        default: null,
    },
});

const emit = defineEmits(['update:open']);

const isOpen = ref(props.open);
const forecast = ref(null);
const loading = ref(false);

const { fetchForecast } = useWeatherAPI();

watch(
    () => props.open,
    (value) => {
        isOpen.value = value;
        if (value && props.locationId) {
            loadForecastData();
        }
    }
);

watch(
    () => props.locationId,
    (value) => {
        if (value && isOpen.value) {
            loadForecastData();
        }
    }
);

watch(isOpen, (value) => {
    emit('update:open', value);
});

const loadForecastData = async () => {
    if (!props.locationId) return;

    loading.value = true;
    forecast.value = await fetchForecast(props.locationId);
    loading.value = false;
};

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
    });
};

const getWeatherDescription = (wmoCode) => {
    // Map WMO codes to descriptions
    if (wmoCode >= 0 && wmoCode <= 3) {
        return 'Clear to partly cloudy';
    } else if (wmoCode >= 4 && wmoCode <= 9) {
        return 'Cloudy';
    } else if ((wmoCode >= 10 && wmoCode <= 12) || (wmoCode >= 40 && wmoCode <= 49)) {
        return 'Foggy';
    } else if ((wmoCode >= 13 && wmoCode <= 19) || (wmoCode >= 50 && wmoCode <= 59)) {
        return 'Drizzle';
    } else if ((wmoCode >= 20 && wmoCode <= 29) || (wmoCode >= 60 && wmoCode <= 69)) {
        return 'Rainy';
    } else if ((wmoCode >= 30 && wmoCode <= 39) || (wmoCode >= 70 && wmoCode <= 79)) {
        return 'Snowy';
    } else if (wmoCode >= 80 && wmoCode <= 99) {
        return 'Thunderstorm';
    }
    return 'Unknown';
};

const closeSidebar = () => {
    isOpen.value = false;
};
</script>
