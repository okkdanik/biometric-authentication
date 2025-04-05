import os
import json
import platform
import requests

log_dir = 'logs/users_data'

ru_regions = {
    'Donetsk', 'Donetsk Oblast'
    'Luhansk', 'Luhansk Oblast'
    'Zaporizhia', 'Kherson',
    'Crimea', 'Republic of Crimea'
}


def get_location_info(ip: str) -> dict:
    try:
        response = requests.get(f'https://ipwho.is/{ip}')
        data = response.json()

        if not data.get('success', False):
            return {"error": "Failed to retrieve location data"}

        region = data.get('region', '')
        country = data.get('country', '')

        for ru_region in ru_regions:
            if ru_region.lower() in region.lower():
                country = 'Russia'
                break

        return {
            'ip': ip,
            'city': data.get('city', ''),
            'region': region,
            'country': country,
        }

    except Exception as e:
        return {'error': str(e)}


def get_os():
    return platform.platform()


def log_successful_login(username, recognition_time, confidence):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, f'{username}.json')

    try:
        ip = requests.get('https://api.ipify.org').text.strip()
    except Exception as e:
        ip = 'Unknown'

    location = get_location_info(ip)
    os_info = get_os()

    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        count = data.get('count', 0)
        data['avg_recognition_time'] = round(
            (data.get('avg_recognition_time', recognition_time) * count + recognition_time) / (count + 1), 3
        )
        data['avg_confidence'] = round(
            (data.get('avg_confidence', confidence) * count + confidence) / (count + 1), 3
        )
        data['count'] = count + 1

    else:
        data = {
            'username': username,
            'location': location,
            'os': os_info,
            'avg_recognition_time': round(recognition_time, 3),
            'avg_confidence': round(confidence, 3),
            'count': 1
        }

    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


