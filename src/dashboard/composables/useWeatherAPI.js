export default function useWeatherAPI() {
    const apiBaseUrl = 'http://localhost:8000';

    const fetchLocations = async () => {
        try {
            console.log('Fetching locations from:', `${apiBaseUrl}/locations`);
            const response = await fetch(`${apiBaseUrl}/locations`);

            if (!response.ok) {
                console.error('Server responded with status:', response.status);
                throw new Error(`Failed to fetch locations: ${response.statusText}`);
            }

            const data = await response.json();
            console.log('Locations data:', data);
            return data;
        } catch (error) {
            console.error('Error fetching locations:', error);
            return [];
        }
    };

    const fetchForecast = async (locationId) => {
        try {
            console.log('Fetching forecast for location ID:', locationId);
            const response = await fetch(`${apiBaseUrl}/forecast/${locationId}`);

            if (!response.ok) {
                console.error('Server responded with status:', response.status);
                throw new Error(`Failed to fetch forecast: ${response.statusText}`);
            }

            const data = await response.json();
            console.log('Forecast data:', data);
            return data;
        } catch (error) {
            console.error('Error fetching forecast:', error);
            return null;
        }
    };

    const addLocation = async (locationData) => {
        try {
            console.log('Adding location:', locationData);
            const response = await fetch(`${apiBaseUrl}/locations`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(locationData),
            });

            if (!response.ok) {
                console.error('Server responded with status:', response.status);
                throw new Error(`Failed to add location: ${response.statusText}`);
            }

            const data = await response.json();
            console.log('Added location data:', data);
            return data;
        } catch (error) {
            console.error('Error adding location:', error);
            return null;
        }
    };

    const removeLocation = async (locationId) => {
        try {
            console.log('Removing location ID:', locationId);
            const response = await fetch(`${apiBaseUrl}/locations/${locationId}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                console.error('Server responded with status:', response.status);
                throw new Error(`Failed to remove location: ${response.statusText}`);
            }

            const data = await response.json();
            console.log('Remove location response:', data);
            return data;
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
