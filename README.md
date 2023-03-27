# Zoom Recording Downloader
A tool written in Python to easily download Zoom Recordings

## Requirements ##
You will need a paid Zoom account. Go to the Zoom Developer Portal to [Create a new app](https://marketplace.zoom.us/develop/create). Then choose the JWT option. Note that this option will become obsolete in a few months and future authentication will need to be revised.

## Installation ##
You can `git clone` this script on your Linux machine or download it via GitHub. Once finished, make sure you update the `JWT_TOKEN` to your specific token.

## Usage ##
1. Run the Python script. 
2. Specify between 1 to 5 years of recordings which you want to retrieve. 
3. Wait for the script to load a list of your recordings. Then select the recording index you want to download.
4. Enter a name for the folder of the selected meeting.
5. Perform step 1 again until you've downloaded all the recordings.

You can also watch the [tutorial video on YouTube](https://www.youtube.com/watch?v=Yh7f_7ud24Y).