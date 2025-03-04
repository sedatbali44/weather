<template>
    <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" :class="iconClass">
        <template v-if="wmoCode === 0">
            <path d="M12 2l10 5-10 5-10-5 10-5z" fill="currentColor" />
            <path d="M12 12l10 5-10 5-10-5 10-5z" fill="currentColor" />
        </template>
        <template v-else-if="wmoCode === 1">
            <path d="M12 2l10 5-10 5-10-5 10-5z" fill="currentColor" opacity="0.7" />
            <path d="M12 12l10 5-10 5-10-5 10-5z" fill="currentColor" opacity="0.5" />
        </template>
        <template v-else-if="wmoCode === 2">
            <path d="M12 2l10 5-10 5-10-5 10-5z" fill="currentColor" opacity="0.5" />
            <path d="M12 12l10 5-10 5-10-5 10-5z" fill="currentColor" opacity="0.3" />
        </template>
        <template v-else-if="wmoCode === 3">
            <path d="M12 2l10 5-10 5-10-5 10-5z" fill="currentColor" opacity="0.3" />
            <path d="M12 12l10 5-10 5-10-5 10-5z" fill="currentColor" opacity="0.1" />
        </template>
    </svg>
</template>

<script>
export default {
    name: 'WeatherIcon',
    props: {
        wmoCode: {
            type: Number,
            default: 0,
        },
    },
    computed: {
        iconClass() {
            switch (this.wmoCode) {
                case 0:
                    return 'text-yellow-400';
                case 1:
                    return 'text-blue-400';
                case 2:
                    return 'text-gray-400';
                case 3:
                    return 'text-gray-500';
                default:
                    return 'text-gray-300';
            }
        },
    },
};
</script>
