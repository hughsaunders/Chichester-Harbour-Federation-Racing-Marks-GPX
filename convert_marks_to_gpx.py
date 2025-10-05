#!/usr/bin/env python3
"""
Convert racing marks JSON data to GPX waypoints format.
"""

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import argparse
import sys
from pathlib import Path


def create_gpx_waypoint(mark_data):
    """Create a GPX waypoint element from mark data."""
    # Create waypoint element
    wpt = ET.Element('wpt')
    wpt.set('lat', mark_data['Latitude'])
    wpt.set('lon', mark_data['Longitude'])
    
    # Add name
    name = ET.SubElement(wpt, 'name')
    name.text = mark_data['MarkName'].strip()
    
    # Add description with mark details
    desc_parts = []
    if 'text1' in mark_data and mark_data['text1']:
        # Clean up HTML entities and tags
        text1_clean = mark_data['text1'].replace('&nbsp;', ' ').replace('<br />', ', ').strip(', ')
        if text1_clean:
            desc_parts.append(text1_clean)
    
    if 'text2' in mark_data and mark_data['text2']:
        desc_parts.append(f"Club: {mark_data['text2']}")
    
    if 'MarkID' in mark_data:
        desc_parts.append(f"ID: {mark_data['MarkID']}")
    
    if desc_parts:
        desc = ET.SubElement(wpt, 'desc')
        desc.text = ' | '.join(desc_parts)
    
    # Add formatted coordinates as comment
    cmt = ET.SubElement(wpt, 'cmt')
    lat_formatted = mark_data.get('LatFormatted', '').replace('&nbsp;', ' ')
    lon_formatted = mark_data.get('LonFormatted', '').replace('&nbsp;', ' ')
    cmt.text = f"{lat_formatted} {lon_formatted}"
    
    # Add symbol based on icon type
    sym = ET.SubElement(wpt, 'sym')
    icon_url = mark_data.get('IconURL', '')
    
    # Map icon types to GPX symbols
    if 'yellow_red' in icon_url:
        sym.text = 'Buoy, Red/Yellow'
    elif 'yellow_green' in icon_url:
        sym.text = 'Buoy, Green/Yellow'
    elif 'buoy_yellow' in icon_url:
        sym.text = 'Buoy, Yellow'
    elif 'buoy_red' in icon_url:
        sym.text = 'Buoy, Red'
    elif 'buoy_green' in icon_url:
        sym.text = 'Buoy, Green'
    elif 'post' in icon_url:
        sym.text = 'Post'
    else:
        sym.text = 'Waypoint'
    
    return wpt


def convert_json_to_gpx(json_file_path, output_file_path=None):
    """Convert JSON marks file to GPX format."""
    
    # Read JSON data
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            marks_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' not found.")
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{json_file_path}': {e}")
        return False
    
    # Create GPX root element
    gpx = ET.Element('gpx')
    gpx.set('version', '1.1')
    gpx.set('creator', 'Racing Marks Converter')
    gpx.set('xmlns', 'http://www.topografix.com/GPX/1/1')
    gpx.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    gpx.set('xsi:schemaLocation', 'http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd')
    
    # Add metadata
    metadata = ET.SubElement(gpx, 'metadata')
    name = ET.SubElement(metadata, 'name')
    name.text = 'Chichester Harbour Racing Marks'
    desc = ET.SubElement(metadata, 'desc')
    desc.text = 'Racing marks and waypoints for Chichester Harbour sailing'
    
    # Convert each mark to a waypoint
    waypoint_count = 0
    for mark in marks_data:
        try:
            wpt = create_gpx_waypoint(mark)
            gpx.append(wpt)
            waypoint_count += 1
        except Exception as e:
            print(f"Warning: Could not process mark {mark.get('MarkName', 'Unknown')}: {e}")
            continue
    
    # Generate output filename if not provided
    if output_file_path is None:
        input_path = Path(json_file_path)
        output_file_path = input_path.parent / f"{input_path.stem}.gpx"
    
    # Write GPX file with pretty formatting
    try:
        rough_string = ET.tostring(gpx, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")
        
        # Remove empty lines
        lines = [line for line in pretty_xml.split('\n') if line.strip()]
        pretty_xml = '\n'.join(lines)
        
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
        
        print(f"Successfully converted {waypoint_count} waypoints to '{output_file_path}'")
        return True
        
    except Exception as e:
        print(f"Error writing GPX file: {e}")
        return False


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(
        description='Convert racing marks JSON to GPX waypoints',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python convert_marks_to_gpx.py marks2.json
  python convert_marks_to_gpx.py marks2.json -o waypoints.gpx
        """
    )
    
    parser.add_argument('input_file', help='Input JSON file containing racing marks')
    parser.add_argument('-o', '--output', help='Output GPX file (default: input_file.gpx)')
    
    args = parser.parse_args()
    
    # Convert the file
    success = convert_json_to_gpx(args.input_file, args.output)
    
    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()
