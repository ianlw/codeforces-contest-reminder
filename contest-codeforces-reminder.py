import requests
import datetime
import time
import os

def get_closest_contest():
    url = "https://codeforces.com/api/contest.list"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        contests = data["result"]
        current_time = time.time()

        # Filtrar solo los concursos futuros
        upcoming_contests = [c for c in contests if c["phase"] == "BEFORE"]

        # Ordenar por fecha de inicio más cercana
        upcoming_contests.sort(key=lambda c: c["startTimeSeconds"])

        if upcoming_contests:
            closest_contest = upcoming_contests[0]
            contest_name = closest_contest["name"]
            start_time = datetime.datetime.fromtimestamp(closest_contest["startTimeSeconds"])

            return contest_name, start_time
    return None, None

def send_notification(title, message):
    os.system(f'dunstify "{title}" "{message}" -i "file:///home/ian/Downloads/Codeforces.colored.svg"')

def main():
    contest_name, start_time = get_closest_contest()

    if contest_name:
        now = datetime.datetime.now()
        time_diff = (start_time - now).total_seconds()
        hours, remainder = divmod(time_diff, 3600)
        minutes, _ = divmod(remainder, 60)
        
        if now.date() == start_time.date():
            send_notification(f'{contest_name}', f"Starts in {int(hours)}h {int(minutes)}m")
        elif now.date() + datetime.timedelta(days=1) == start_time.date():
            send_notification(f'{contest_name}', f"Starts tomorrow at {start_time.strftime('%H:%M')}")
        elif now.isocalendar()[1] == start_time.isocalendar()[1]:
            day_name = start_time.strftime('%A')
            send_notification(f'{contest_name}', f"Starts this {day_name} at {start_time.strftime('%H:%M')}")
        else:
            send_notification(f'{contest_name}', f"Starts on {start_time.strftime('%A %d %B')} at {start_time.strftime('%H:%M')}")
    else:
        print("No hay concursos próximos.")

if __name__ == "__main__":
    main()
