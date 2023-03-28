        import os
        import json
        import asyncio
        import aiohttp
        import requests
        import time
        import pathlib
        from datetime import datetime, timedelta
        from typing import List, Tuple
         
        API_BASE_URL = "https://api.zoom.us/v2"
        # UPDATE this to your JWT token
        JWT_TOKEN = "eyJxxxxxxx"
         
        headers = {
            "Authorization": f"Bearer {JWT_TOKEN}",
            "Content-Type": "application/json",
        }
         
        def download_file(url: str, filename: str, access_token: str, file_size: int) -> None:
            url = f"{url}?access_token={access_token}"
            bytes_downloaded = 0
            print(f"Downloading {filename}")
           
            with requests.get(url, stream=True) as resp:
                resp.raise_for_status()
                with open(filename, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            bytes_downloaded += len(chunk)
                            progress = (bytes_downloaded / file_size) * 100
                            print(f" {progress:.2f}% complete", end="\r")
            print(f"Downloaded {filename}: 100% complete")
         
        def download_files(urls: List[Tuple[str, str, str, int]]) -> None:
            for url, filename, access_token, file_size in urls:
                download_file(url, filename, access_token, file_size)
                time.sleep(0.2)  # Add a delay between requests to avoid exceeding the rate limit
           
        def get_recordings(page_size: int = 10) -> List[dict]:
            years = int(input("Enter years of recordings to retrieve: "))
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=365 * years)
            print("One moment. Loading your recordings...")
             
            recordings = []
            delay = 0.2  # 200 ms delay between requests to stay within the 10 requests per second limit
         
            while end_date > start_date:
                to_date = end_date
                from_date = end_date - timedelta(days=30)
         
                if from_date < start_date:
                    from_date = start_date
         
                print(f"Fetching from {from_date.strftime('%Y-%m-%d')} to {to_date.strftime('%Y-%m-%d')}")
               
                url = f"{API_BASE_URL}/users/me/recordings?page_size={page_size}&from={from_date.strftime('%Y-%m-%d')}&to={to_date.strftime('%Y-%m-%d')}"
                response = requests.get(url, headers=headers)
         
                if response.status_code != 200:
                    print("Failed to get recordings")
                    return []
         
                new_recordings = response.json().get("meetings", [])
                recordings.extend(new_recordings)
         
                # Break out of the loop if the number of recordings exceeds the page_size
                if len(recordings) >= page_size:
                    break
         
                end_date = from_date
                time.sleep(delay)  # Add a delay between requests to avoid exceeding the rate limit
         
            print("FETCH COMPLETE!")
            return recordings[:page_size]

        def main() -> None:
            print("Welcome to Zoom Downloader Tool")
            print("By Dominick Lee")
            recordings = get_recordings()

            while True:
                print("----------------------SELECT A RECORDING-------------------------")
                for idx, rec in enumerate(recordings, 1):
                    print(f"{idx}. {rec['topic']} ({rec['start_time']})")

                print("-----------------------------------------------------------------")
                print("Enter 'q' to quit or")
                meeting_idx = input("Enter the meeting index to download: ")

                if meeting_idx.lower() == 'q':
                    break

                meeting_idx = int(meeting_idx) - 1

                if 0 <= meeting_idx < len(recordings):
                    meeting = recordings[meeting_idx]
                    folder_name = input("Enter the folder name for this meeting: ")
                    home_dir = str(pathlib.Path.home())
                    folder_path = os.path.join(home_dir, "Videos/ZoomRecords", folder_name)

                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)

                    files = meeting.get("recording_files", [])
                    download_list = []

                    for f in files:
                        if f["file_type"] in ["MP4", "M4A", "CHAT"]:
                            download_url = f["download_url"]
                            file_ext = f["file_type"].lower()
                            if file_ext == "chat":
                                file_ext = "txt"
                            recording_type = f["recording_type"]
                            file_naming = "GMT" + f["recording_start"].replace(":", "") + "_" + recording_type
                     
                            file_name = f"{file_naming}.{file_ext}"
                            file_path = os.path.join(folder_path, file_name)
                            file_size = int(f["file_size"])
                            download_list.append((download_url, file_path, JWT_TOKEN, file_size))
                    
                    download_files(download_list)
                    print("All files downloaded.")
                else:
                    print("Invalid index. Exiting.")
         
        if __name__ == "__main__":
            main()
         
