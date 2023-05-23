## App Usage Guide

### How to Use the App

To run the app, follow these steps:

1. Connect an external camera.
2. Execute `main.py`.
3. A window will pop up, displaying several buttons.

#### Scan

Click the "Scan" button to scan new QR codes. The window will show a message informing you about the status of the most recent QR code you've scanned and the total number of QR codes in the database.

#### Switch camera

Click the "Switch camera" button to switch between the web camera and an external camera. The default option is an external camera.

#### Map

To generate images of the grid that show the pieces a team put up in their matches, follow these steps:

1. Enter a team number in the box above the button.
2. Click the "Map" button.
3. The file will open in your browser.

#### Update

To update the stats for specific teams in the same column, follow these steps:

1. Enter a team number in the box above the button.
2. Click the "Update" button.

Note: All displayed stats are averages, except for the last two: autonomous and endgame charging. Their format is engaged-docked-other. For example, if the record is 1-2-3, it means they got engaged once, docked twice, and did something else (park or none) three times.

### Meeting Time

Before starting your scouting meeting, run `meeting_prep.py`. This file will generate spreadsheets with average stats and match-by-match stats for every team.

Team 624 uses Google Forms for pit scouting, and the last question is always a picture of the robot. To attach pictures to each team's page on the spreadsheet, place a file named `pit.csv` in the same folder as the app.

Additionally, each team will receive two HTML files showing their contributions to the grid in every match. The app also includes a graphing feature to check the progression of every team throughout the tournament.

### `api.py` File

The `api.py` file contains various functions that allow you to gain more insights into a competition and check your data using The Blue Alliance, Statbotics, and other websites. Most of these functions were rarely used but can be added if needed.

The following functions have been used this season:

#### `export_links`

This function generates a CSV file with estimations of how many links each team contributes. It uses the same algorithms as OPR.

#### `check_db`

This function checks every input against TBA. It can only detect false positives when a scout indicates that a piece was placed when it actually wasn't.

To use any of these functions, call `TBA().[function name]()` in any other file.

### Other Notes

Before using the app, please complete the following steps in the `config.json` file:

1. Fill in any blank spaces, such as the TBA key, number of quals, etc.
2. Use the `scouts.json` file to keep track of who scouted each match.