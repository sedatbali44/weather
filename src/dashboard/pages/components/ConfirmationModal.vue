<!-- frontend/components/weather/ConfirmationModal.vue -->
<template>
    <UModal v-model="isOpen">
        <UCard>
            <template #header>
                <div class="flex items-center justify-between">
                    <h3 class="text-lg font-semibold">{{ title }}</h3>
                    <UButton icon="i-heroicons-x-mark" color="gray" variant="ghost" @click="closeModal" />
                </div>
            </template>

            <div class="py-4">
                <p>{{ message }}</p>
            </div>

            <template #footer>
                <div class="flex justify-end gap-2">
                    <UButton variant="ghost" @click="closeModal"> Cancel </UButton>
                    <UButton color="red" @click="confirmAction"> Remove </UButton>
                </div>
            </template>
        </UCard>
    </UModal>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
    open: {
        type: Boolean,
        default: false,
    },
    title: {
        type: String,
        default: 'Confirmation',
    },
    message: {
        type: String,
        default: 'Are you sure you want to perform this action?',
    },
});

const emit = defineEmits(['update:open', 'confirm']);

const isOpen = ref(props.open);

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
};

const confirmAction = () => {
    emit('confirm');
    closeModal();
};
</script>
