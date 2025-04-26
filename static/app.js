async function getWeather() {
    const location = document.getElementById('location').value;
    const resultDiv = document.getElementById('weather-result');
    
    try {
        const response = await fetch(`/api/weather?location=${encodeURIComponent(location)}`);
        const data = await response.json();
        
        if (data.error) {
            // Show detailed error from backend
            let errorMsg = `Error: ${data.error}`;
            if (data.api_response && data.api_response.message) {
                errorMsg += ` (${data.api_response.message})`;
            }
            resultDiv.innerHTML = errorMsg;
            console.error('Backend error details:', data);
            return;
        }
        
        // Display weather data
        resultDiv.innerHTML = `
            <h2>${data.city}</h2>
            <p>Temperature: ${data.temperature}°C</p>
            <p>Conditions: ${data.conditions}</p>
            <p>Humidity: ${data.humidity}%</p>
            <img src="https://openweathermap.org/img/wn/${data.icon}.png" alt="Weather icon">
        `;
        
    } catch (error) {
        resultDiv.innerHTML = `Network error: ${error.message}`;
        console.error('Fetch error:', error);
    }
}