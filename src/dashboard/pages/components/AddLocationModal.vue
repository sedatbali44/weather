<!-- src/dashboard/pages/components/AddLocationModal.vue -->
<template>
    <UModal v-model="isOpen" prevent-close>
        <UCard>
            <template #header>
                <div class="flex items-center justify-between">
                    <h3 class="text-lg font-semibold">Add Location</h3>
                    <UButton icon="i-heroicons-x-mark" color="gray" variant="ghost" @click="closeModal" />
                </div>
            </template>

            <div class="py-4">
                <UFormGroup label="Search for a location" required>
                    <USelect
                        v-model="selectedLocation"
                        :options="availableLocations"
                        placeholder="Start typing to search"
                        searchable
                        option-attribute="name"
                        :ui="{ option: { base: 'flex items-center gap-2' } }"
                    >
                        <template #option="{ option }">
                            <div>
                                <div>{{ option.name }}</div>
                                <div class="text-gray-500 text-xs">
                                    Lat: {{ option.latitude.toFixed(2) }}, Long: {{ option.longitude.toFixed(2) }}
                                </div>
                            </div>
                        </template>
                    </USelect>
                </UFormGroup>
            </div>

            <template #footer>
                <div class="flex justify-end gap-2">
                    <UButton variant="ghost" @click="closeModal"> Cancel </UButton>
                    <UButton color="primary" :disabled="!selectedLocation" @click="addLocation"> Add </UButton>
                </div>
            </template>
        </UCard>
    </UModal>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useWeatherAPI } from '~/composables/useWeatherAPI';

const props = defineProps({
    open: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(['update:open', 'location-added']);

const isOpen = ref(props.open);
const selectedLocation = ref(null);

// This would be the predefined list of locations
// https://gist.github.com/ofou/df09a6834a8421b4f376c875194915c9
const availableLocations = ref([
    { name: 'New York', latitude: 40.7128, longitude: -74.006, population: 8804190, capitalType: 'state' },
    { name: 'London', latitude: 51.5074, longitude: -0.1278, population: 8961989, capitalType: 'primary' },
    { name: 'Paris', latitude: 48.8566, longitude: 2.3522, population: 2140526, capitalType: 'primary' },
    { name: 'Tokyo', latitude: 35.6762, longitude: 139.6503, population: 13929286, capitalType: 'primary' },
    { name: 'Sydney', latitude: -33.8688, longitude: 151.2093, population: 5312163, capitalType: 'state' },
    { name: 'Berlin', latitude: 52.52, longitude: 13.405, population: 3769495, capitalType: 'primary' },
    { name: 'Rome', latitude: 41.9028, longitude: 12.4964, population: 2872800, capitalType: 'primary' },
    { name: 'Madrid', latitude: 40.4168, longitude: -3.7038, population: 3266126, capitalType: 'primary' },
    { name: 'Moscow', latitude: 55.7558, longitude: 37.6173, population: 12537954, capitalType: 'primary' },
    { name: 'Beijing', latitude: 39.9042, longitude: 116.4074, population: 21542000, capitalType: 'primary' },
]);

const { addLocation: apiAddLocation } = useWeatherAPI();

watch(
    () => props.open,
    (value) => {
        isOpen.value = value;
    }
);

watch(isOpen, (value) => {
    emit('update:open', value);
});

const closeModal = () => {
    isOpen.value = false;
    selectedLocation.value = null;
};

const addLocation = async () => {
    if (selectedLocation.value) {
        try {
            await apiAddLocation({
                name: selectedLocation.value.name,
                latitude: selectedLocation.value.latitude,
                longitude: selectedLocation.value.longitude,
                population: selectedLocation.value.population,
                capitalType: selectedLocation.value.capitalType,
            });

            emit('location-added');
            closeModal();
        } catch (error) {
            console.error('Failed to add location:', error);
            // Could add error handling UI here
        }
    }
};
</script>
