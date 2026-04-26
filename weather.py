import requests
import os
import imgkit
from datetime import datetime

# Configuration
API_KEY = os.getenv("API_KEY")
LAT = "-33.9006" # Enmore
LON = "151.1732"

def get_weather():
    # 1. Fetch Data (Using the stable 2.5 API)
    curr_url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&units=metric&appid={API_KEY}"
    fore_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&units=metric&appid={API_KEY}"
    
    curr_res = requests.get(curr_url).json()
    fore_res = requests.get(fore_url).json()

    if curr_res.get('cod') != 200:
        raise Exception(f"API Error: {curr_res.get('message')}")

    current = curr_res
    hourly = fore_res['list'][:8] 
    
    # Using more stable symbols to avoid encoding glitches on some E-ink systems
    icon_map = {"Clear": "SUN", "Clouds": "CLOUD", "Rain": "RAIN", "Drizzle": "DRIZ", "Thunderstorm": "STORM"}

    # Added <meta charset='UTF-8'> which is the primary fix for the 'Â' symbols
    html_content = f"""
    <!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset='UTF-8'>
        <style>
            :root {{ --bg: #FFFFFF; --text: #000000; --bom-blue: #003057; --bom-light-blue: #D0E4F2; }}
            body {{ margin: 0; padding: 0; width: 800px; height: 480px; background: var(--bg); font-family: sans-serif; overflow: hidden; }}
            .screen {{ width: 800px; height: 480px; border: 2px solid #000; display: flex; flex-direction: column; }}
            .summary {{ height: 130px; display: flex; align-items: center; padding: 0 30px; border-bottom: 5px solid var(--bom-blue); }}
            .temp-main {{ font-size: 80px; font-weight: 900; margin-right: 30px; }}
            table {{ width: 100%; border-collapse: collapse; table-layout: fixed; flex-grow: 1; }}
            th, td {{ border: 1px solid #999; text-align: center; font-size: 14px; padding: 8px 0; }}
            th {{ background: var(--bom-light-blue); color: var(--bom-blue); font-weight: bold; }}
            .label {{ width: 100px; text-align: left; padding-left: 10px; background: #eee; font-weight: bold; }}
            .temp-row {{ color: #CC0000; font-weight: bold; font-size: 18px; }}
        </style>
    </head>
    <body>
        <div class="screen">
            <div class="summary">
                <div class="temp-main">{round(current['main']['temp'])}°</div>
                <div style="font-size: 40px; font-weight:bold; margin-right: 25px;">{icon_map.get(current['weather'][0]['main'], "FAIR")}</div>
                <div>
                    <strong style="font-size: 24px;">{current['weather'][0]['description'].title()}</strong><br>
                    <span>Feels like {round(current['main']['feels_like'])}° | Hum: {current['main']['humidity']}%</span>
                </div>
            </div>
            <table>
                <tr>
                    <th class="label">Time</th>
                    {" ".join([f"<th>{datetime.fromtimestamp(h['dt']).strftime('%-I%p').lower()}</th>" for h in hourly])}
                </tr>
                <tr>
                    <td class="label">Forecast</td>
                    {" ".join([f"<td>{icon_map.get(h['weather'][0]['main'], 'FAIR')}</td>" for h in hourly])}
                </tr>
                <tr class="temp-row">
                    <td class="label">Temp °C</td>
                    {" ".join([f"<td>{round(h['main']['temp'])}°</td>" for h in hourly])}
                </tr>
                <tr style="color: #0077be; font-weight: bold;">
                    <td class="label">Rain %</td>
                    {" ".join([f"<td>{int(h.get('pop', 0)*100)}%</td>" for h in hourly])}
                </tr>
                <tr>
                    <td class="label">Wind km/h</td>
                    {" ".join([f"<td>{round(h['wind']['speed'] * 3.6)}</td>" for h in hourly])}
                </tr>
            </table>
            <div style="background: var(--bom-blue); color: white; padding: 5px 20px; font-size: 14px;">
                Enmore, NSW | Updated: {datetime.now().strftime('%H:%M')}
            </div>
        </div>
    </body>
    </html>
    """
    
    # Save with explicit utf-8 encoding
    with open("dashboard.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    options = {
        'width': 800, 
        'height': 480, 
        'disable-smart-width': '', 
        'quiet': '',
        'encoding': 'UTF-8' # Force imgkit to use UTF-8
    }
    imgkit.from_file('dashboard.html', 'weather.png', options=options)

if __name__ == "__main__":
    get_weather()
