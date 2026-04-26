import requests
import os
import imgkit
from datetime import datetime

# Configuration
API_KEY = os.getenv("API_KEY")
LAT = "-33.9006" # Enmore, NSW
LON = "151.1732"

def get_weather():
    # 1. Fetch Data
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={LAT}&lon={LON}&exclude=minutely,daily&units=metric&appid={API_KEY}"
    response = requests.get(url).json()
    
    current = response['current']
    hourly = response['hourly'][:8] # Next 8 hours
    
    # 2. Map Icons
    icon_map = {
        "Clear": "☀️", 
        "Clouds": "☁️", 
        "Rain": "🌧️", 
        "Drizzle": "🌦️", 
        "Thunderstorm": "⛈️",
        "Snow": "❄️"
    }

    # 3. Build HTML (800x480 Optimized)
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            :root {{ --bg: #FFFFFF; --text: #000000; --bom-blue: #003057; --bom-light-blue: #D0E4F2; }}
            body {{ margin: 0; padding: 0; width: 800px; height: 480px; background: var(--bg); font-family: sans-serif; overflow: hidden; }}
            .screen {{ width: 800px; height: 480px; border: 2px solid #000; display: flex; flex-direction: column; }}
            .summary {{ height: 130px; display: flex; align-items: center; padding: 0 30px; border-bottom: 5px solid var(--bom-blue); }}
            .temp-main {{ font-size: 80px; font-weight: 900; margin-right: 30px; }}
            table {{ width: 100%; border-collapse: collapse; table-layout: fixed; flex-grow: 1; }}
            th, td {{ border: 1px solid #999; text-align: center; font-size: 16px; padding: 10px 0; }}
            th {{ background: var(--bom-light-blue); color: var(--bom-blue); font-weight: bold; }}
            .label {{ width: 120px; text-align: left; padding-left: 15px; background: #eeeeee; font-weight: bold; color: var(--bom-blue); }}
            .temp-row {{ color: #CC0000; font-weight: bold; font-size: 20px; }}
            .rain-row {{ color: #0077be; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="screen">
            <div class="summary">
                <div class="temp-main">{round(current['temp'])}°</div>
                <div style="font-size: 60px; margin-right: 25px;">{icon_map.get(current['weather'][0]['main'], "🌤️")}</div>
                <div>
                    <strong style="font-size: 28px;">{current['weather'][0]['description'].title()}</strong><br>
                    <span style="font-size: 20px;">Feels like {round(current['feels_like'])}° | Hum: {current['humidity']}%</span>
                </div>
            </div>
            <table>
                <tr>
                    <th class="label">Time</th>
                    {" ".join([f"<th>{datetime.fromtimestamp(h['dt']).strftime('%-I%p').lower()}</th>" for h in hourly])}
                </tr>
                <tr>
                    <td class="label">Forecast</td>
                    {" ".join([f"<td>{icon_map.get(h['weather'][0]['main'], '🌤️')}</td>" for h in hourly])}
                </tr>
                <tr class="temp-row">
                    <td class="label">Temp °C</td>
                    {" ".join([f"<td>{round(h['temp'])}°</td>" for h in hourly])}
                </tr>
                <tr class="rain-row">
                    <td class="label">Rain %</td>
                    {" ".join([f"<td>{int(h.get('pop', 0)*100)}%</td>" for h in hourly])}
                </tr>
                <tr style="font-size: 14px;">
                    <td class="label">Wind km/h</td>
                    {" ".join([f"<td>{round(h['wind_speed'] * 3.6)}</td>" for h in hourly])}
                </tr>
            </table>
            <div style="background: var(--bom-blue); color: white; padding: 5px 20px; font-size: 14px; font-weight: bold;">
                Enmore, NSW | Updated: {datetime.now().strftime('%H:%M')}
            </div>
        </div>
    </body>
    </html>
    """
    
    # 4. Save to Image
    with open("dashboard.html", "w") as f:
        f.write(html_content)

    options = {'width': 800, 'height': 480, 'disable-smart-width': ''}
    imgkit.from_file('dashboard.html', 'weather.png', options=options)

if __name__ == "__main__":
    get_weather()
