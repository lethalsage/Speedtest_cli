import speedtest
from colorama import Fore, Style
from alive_progress import alive_bar
import time

def color_speed(speed):
    if speed > 50:
        return Fore.GREEN
    elif 20 <= speed <= 50:
        return Fore.YELLOW
    else:
        return Fore.RED

def display_speed(speed, label):
    color = color_speed(speed)
    bar_length = int(speed / 10)  # Scale the bar length
    bar = '█' * bar_length + '-' * (10 - bar_length)
    print(f"{label}: {color}{speed:.2f} Mbps {bar}{Style.RESET_ALL}")

def test_speed(progress_bar, st, speed_type):
    speed = 0
    if speed_type == "download":
        speed = st.download() / 1_000_000  # Convert to Mbps
    elif speed_type == "upload":
        speed = st.upload() / 1_000_000  # Convert to Mbps
    for _ in range(100):
        time.sleep(0.01)  # Showing progress
        progress_bar()
    return speed

def main():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()  # Check if the network is connected
    except speedtest.ConfigRetrievalError:
        print("Network is not connected.")
        display_speed(0, "Download Speed")
        display_speed(0, "Upload Speed")
        return

    try:
        print("Testing download speed...")
        with alive_bar(100, title="Calculating speed", bar="smooth", spinner="dots_waves") as bar:
            download_speed = test_speed(bar, st, "download")
        display_speed(download_speed, "Download Speed")

        print("Testing upload speed...")
        with alive_bar(100, title="Calculating speed", bar="smooth", spinner="dots_waves") as bar:
            upload_speed = test_speed(bar, st, "upload")
        display_speed(upload_speed, "Upload Speed")
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user.Why?")

if __name__ == "__main__":
    main()



