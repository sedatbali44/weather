export function getWeatherIcon(wmoCode) {
    // WMO Weather codes: https://open-meteo.com/en/docs
    if (wmoCode >= 0 && wmoCode <= 3) {
        return 'sunny.svg'; // Clear to partly cloudy
    } else if (wmoCode >= 4 && wmoCode <= 9) {
        return 'partly-cloudy.svg'; // Cloudy
    } else if ((wmoCode >= 10 && wmoCode <= 12) || (wmoCode >= 40 && wmoCode <= 49)) {
        return 'foggy.svg'; // Fog
    } else if ((wmoCode >= 13 && wmoCode <= 19) || (wmoCode >= 50 && wmoCode <= 59)) {
        return 'rainy.svg'; // Drizzle
    } else if ((wmoCode >= 20 && wmoCode <= 29) || (wmoCode >= 60 && wmoCode <= 69)) {
        return 'rainy.svg'; // Rain
    } else if ((wmoCode >= 30 && wmoCode <= 39) || (wmoCode >= 70 && wmoCode <= 79)) {
        return 'snowy.svg'; // Snow
    } else if (wmoCode >= 80 && wmoCode <= 99) {
        return 'thunderstorm.svg'; // Thunderstorm
    }
    return 'partly-cloudy.svg'; // Default
}
