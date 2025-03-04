// utils/weather.js
export const getWeatherIcon = (wmoCode) => {
    // Map WMO weather codes to icon names
    // Based on https://open-meteo.com/en/docs (WMO Weather interpretation codes)
    const codeMap = {
        0: 'sun', // Clear sky
        1: 'sun', // Mainly clear
        2: 'cloud-sun', // Partly cloudy
        3: 'cloud', // Overcast
        45: 'fog', // Fog
        48: 'fog', // Depositing rime fog
        51: 'cloud-drizzle', // Light drizzle
        53: 'cloud-drizzle', // Moderate drizzle
        55: 'cloud-drizzle', // Dense drizzle
        56: 'cloud-snow', // Light freezing drizzle
        57: 'cloud-snow', // Dense freezing drizzle
        61: 'cloud-rain', // Slight rain
        63: 'cloud-rain', // Moderate rain
        65: 'cloud-rain', // Heavy rain
        66: 'cloud-rain', // Light freezing rain
        67: 'cloud-rain', // Heavy freezing rain
        71: 'cloud-snow', // Slight snow fall
        73: 'cloud-snow', // Moderate snow fall
        75: 'cloud-snow', // Heavy snow fall
        77: 'cloud-snow', // Snow grains
        80: 'cloud-rain', // Slight rain showers
        81: 'cloud-rain', // Moderate rain showers
        82: 'cloud-rain', // Violent rain showers
        85: 'cloud-snow', // Slight snow showers
        86: 'cloud-snow', // Heavy snow showers
        95: 'cloud-lightning', // Thunderstorm
        96: 'cloud-lightning', // Thunderstorm with slight hail
        99: 'cloud-lightning', // Thunderstorm with heavy hail
    };

    return codeMap[wmoCode] || 'cloud';
};

export const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
};
