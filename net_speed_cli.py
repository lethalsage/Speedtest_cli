import speedtest
from colorama import Fore, Style
from alive_progress import alive_bar
import time
import threading

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

def test_speed(st, speed_type, results):
    speed = 0
    if speed_type == "download":
        speed = st.download() / 1_000_000  # Convert to Mbps
    elif speed_type == "upload":
        speed = st.upload() / 1_000_000  # Convert to Mbps
    results[speed_type] = speed

def main():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()  # Check if the network is connected
    except speedtest.ConfigRetrievalError:
        print("Network is not connected.")
        display_speed(0, "Download Speed")
        display_speed(0, "Upload Speed")
        return

    results = {}

    download_thread = threading.Thread(target=test_speed, args=(st, "download", results))
    upload_thread = threading.Thread(target=test_speed, args=(st, "upload", results))

    print("Testing download and upload speeds...")

    download_thread.start()
    upload_thread.start()

    with alive_bar(100, title="Calculating download speed", bar="smooth", spinner="dots_waves") as bar:
        for _ in range(100):
            time.sleep(0.01)  # show progress
            bar()

    download_thread.join()

    with alive_bar(100, title="Calculating upload speed", bar="smooth", spinner="dots_waves") as bar:
        for _ in range(100):
            time.sleep(0.01)  # show progress
            bar()

    upload_thread.join()

    display_speed(results["download"], "Download Speed")
    display_speed(results["upload"], "Upload Speed")

if __name__ == "__main__":
    main()
