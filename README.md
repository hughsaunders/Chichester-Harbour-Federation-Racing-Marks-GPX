# Chichester Harbor Federation Racing Marks
This repo contains a gpx file of all the 2025 racing marks, and a script to generate it.
The data comes from https://sailingclubsoftware.com/charts/chifed?0.6783275766942094
Specifically the JSON response from POST https://sailingclubsoftware.com/charts/chart.aspx/GetMarks
Which is stored in marks.json. This contains the majority of the json in a single string, which is decoded into [marks2.json](marks2.json).
A PDF of the data is available at https://www.chifed.org/federation-racing-marks/

[marks2.json](marks2.json) is then converted to [marks2.gpx](marks2.gpx) using the [supplied python script](convert_marks_to_gpx.py).

## Racing Marks to GPX Converter Python Script Instructions

This Python script converts JSON data of racing marks into GPX waypoint format that can be imported into GPS devices and navigation software.

## Usage

### Basic Usage
```bash
python3 convert_marks_to_gpx.py marks2.json
```
This will create a file called `marks2.gpx` in the same directory.

### Specify Output File
```bash
python3 convert_marks_to_gpx.py marks2.json -o my_waypoints.gpx
```

### Help
```bash
python3 convert_marks_to_gpx.py --help
```

## Output Format

The script converts each racing mark into a GPX waypoint with:

- **Name**: The mark name (e.g., "Astra", "Baker")
- **Coordinates**: Latitude and longitude from the JSON data
- **Description**: Includes rounding instructions, club, and mark ID
- **Comment**: Formatted coordinates in degrees/minutes
- **Symbol**: Appropriate GPX symbol based on the buoy type:
  - Yellow/Red buoys → "Buoy, Red/Yellow"
  - Yellow/Green buoys → "Buoy, Green/Yellow"
  - Yellow buoys → "Buoy, Yellow"
  - Posts → "Post"
  - Others → "Waypoint"

## Example Output

```xml
<wpt lat="50.79851667" lon="-0.901133333">
  <name>Astra</name>
  <desc>Round to port | Club: TISC | ID: 1192</desc>
  <cmt>50 47.911N 00 54.068W</cmt>
  <sym>Buoy, Red/Yellow</sym>
</wpt>
```

## Compatibility

The generated GPX files are compatible with:
- Garmin GPS devices
- Marine navigation software (OpenCPN, SeaClear, etc.)
- Mobile apps (Navionics, iNavX, etc.)
- Google Earth
- Most GPS and mapping applications

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Files Generated

Running the script on `marks2.json` created:
- `marks2.gpx` - GPX file with 80 waypoints representing all the racing marks

You can now import this GPX file into your preferred navigation software or GPS device.
