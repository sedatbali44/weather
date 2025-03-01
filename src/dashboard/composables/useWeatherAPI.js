import { ref } from 'vue';

export const useWeatherAPI = () => {
    const baseURL = 'http://localhost:8000';

    const fetchLocations = async () => {
        try {
            const response = await fetch(`${baseURL}/locations`);
            if (!response.ok) {
                throw new Error(`Failed to fetch locations: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching locations:', error);
            return [];
        }
    };

    /**
     * Fetches detailed 7-day forecast for a specific location
     */
    const fetchForecast = async (locationId) => {
        try {
            const response = await fetch(`${baseURL}/forecast/${locationId}`);
            if (!response.ok) {
                throw new Error(`Failed to fetch forecast: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching forecast:', error);
            return null;
        }
    };

    /**
     * Adds a new location to the database
     */
    const addLocation = async (locationData) => {
        try {
            const response = await fetch(`${baseURL}/locations`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: locationData.name,
                    latitude: locationData.latitude,
                    longitude: locationData.longitude,
                    country: locationData.country || '',
                    population: locationData.population || 0,
                    capitalType: locationData.capitalType || 'city',
                }),
            });

            if (!response.ok) {
                throw new Error(`Failed to add location: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error adding location:', error);
            throw error;
        }
    };

    /**
     * Removes a location from the database
     */
    const removeLocation = async (locationId) => {
        try {
            const response = await fetch(`${baseURL}/locations/${locationId}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error(`Failed to delete location: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error removing location:', error);
            throw error;
        }
    };

    return {
        fetchLocations,
        fetchForecast,
        addLocation,
        removeLocation,
    };
};
