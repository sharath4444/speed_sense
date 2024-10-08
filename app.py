import streamlit as st
import speedtest
import time

# Function to categorize speed
def categorize_speed(download_speed):
    if download_speed < 5:
        return "Poor"
    elif download_speed < 25:
        return "Medium"
    else:
        return "Good"

# Function to check speed with a countdown timer
def check_speed():
    try:
        st.write("Finding the best server and checking your internet speed...")

        # Display a placeholder for the countdown
        countdown_placeholder = st.empty()

        # Set a countdown of 35 seconds (you can adjust this time)
        countdown_time = 35

        # Simulate the countdown
        for remaining_time in range(countdown_time, 0, -1):
            countdown_placeholder.write(f"Time remaining: {remaining_time} seconds")
            time.sleep(1)
        
        # Perform the speed test step by step
        speed = speedtest.Speedtest()
        speed.get_best_server()

        # Create placeholders for each metric
        download_placeholder = st.empty()
        upload_placeholder = st.empty()
        ping_placeholder = st.empty()

        # Step 1: Check download speed and display
        download_speed = speed.download() / 1_000_000  # Convert to Mbps
        download_placeholder.metric(label="Download Speed", value=f"{download_speed:.2f} Mbps")
        
        # Step 2: Check upload speed and display
        upload_speed = speed.upload() / 1_000_000  # Convert to Mbps
        upload_placeholder.metric(label="Upload Speed", value=f"{upload_speed:.2f} Mbps")
        
        # Step 3: Check ping and display
        ping = speed.results.ping
        ping_placeholder.metric(label="Ping", value=f"{ping:.2f} ms")
        
        return download_speed, upload_speed, ping
    except speedtest.ConfigRetrievalError:
        st.error("Failed to retrieve speed test configuration. Please check your internet connection.")
        return None, None, None
    except speedtest.NoMatchedServers:
        st.error("No servers available for speed test.")
        return None, None, None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None, None, None

# Streamlit interface
st.title("Internet Speed Checker")

if st.button('Check Speed'):
    download, upload, ping = check_speed()

    if download is not None:
        speed_category = categorize_speed(download)
        
        # Show speed status
        st.write(f"Internet Speed Status: **{speed_category}**")
    else:
        st.warning("Speed test could not be completed.")
