// frontend/composables/useWeatherAPI.js
export default function useWeatherAPI() {
    const apiBaseUrl = 'http://localhost:8000';

    const fetchLocations = async () => {
        try {
            const response = await fetch(`${apiBaseUrl}/locations`);
            if (!response.ok) throw new Error('Failed to fetch locations');
            return await response.json();
        } catch (error) {
            console.error('Error fetching locations:', error);
            return [];
        }
    };

    const fetchForecast = async (locationId) => {
        try {
            const response = await fetch(`${apiBaseUrl}/forecast/${locationId}`);
            if (!response.ok) throw new Error('Failed to fetch forecast');
            return await response.json();
        } catch (error) {
            console.error('Error fetching forecast:', error);
            return null;
        }
    };

    const addLocation = async (locationData) => {
        try {
            const response = await fetch(`${apiBaseUrl}/locations`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(locationData),
            });

            if (!response.ok) throw new Error('Failed to add location');
            return await response.json();
        } catch (error) {
            console.error('Error adding location:', error);
            return null;
        }
    };

    const removeLocation = async (locationId) => {
        try {
            const response = await fetch(`${apiBaseUrl}/locations/${locationId}`, {
                method: 'DELETE',
            });

            if (!response.ok) throw new Error('Failed to remove location');
            return await response.json();
        } catch (error) {
            console.error('Error removing location:', error);
            return null;
        }
    };

    return {
        fetchLocations,
        fetchForecast,
        addLocation,
        removeLocation,
    };
}
