export const useApi = () => {
    const config = useRuntimeConfig();
    const baseUrl = config.public.apiBaseUrl || 'http://localhost:8000';

    const getLocations = async () => {
        try {
            const response = await fetch(`${baseUrl}/locations`);
            if (!response.ok) {
                throw new Error('Failed to fetch locations');
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching locations:', error);
            return [];
        }
    };

    const addLocation = async (location) => {
        try {
            const response = await fetch(`${baseUrl}/locations`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(location),
            });

            if (!response.ok) {
                throw new Error('Failed to add location');
            }
            return await response.json();
        } catch (error) {
            console.error('Error adding location:', error);
            throw error;
        }
    };

    const deleteLocation = async (id) => {
        try {
            const response = await fetch(`${baseUrl}/locations/${id}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error('Failed to delete location');
            }
            return await response.json();
        } catch (error) {
            console.error('Error deleting location:', error);
            throw error;
        }
    };

    const getForecast = async (locationId) => {
        try {
            const response = await fetch(`${baseUrl}/forecast/${locationId}`);
            if (!response.ok) {
                throw new Error('Failed to fetch forecast');
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching forecast:', error);
            throw error;
        }
    };

    return {
        getLocations,
        addLocation,
        deleteLocation,
        getForecast,
    };
};
