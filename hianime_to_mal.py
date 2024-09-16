import xml.etree.ElementTree as ET

def transform_xml(input_file, output_file):
    # Parse the input XML
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Create the new root structure
    new_root = ET.Element('myanimelist')

    # Convert folder data from original XML to new format
    for folder in root.findall('folder'):
        category_name = folder.find('name').text
        for item in folder.find('data').findall('item'):
            anime = ET.SubElement(new_root, 'anime')
            ET.SubElement(anime, 'series_animedb_id').text = item.find('link').text.split('/')[-1]
            ET.SubElement(anime, 'series_title').text = f"<![CDATA[{item.find('name').text}]]>"
            ET.SubElement(anime, 'my_watched_episodes').text = "0"
            ET.SubElement(anime, 'my_start_date').text = "0000-00-00"
            ET.SubElement(anime, 'my_finish_date').text = "0000-00-00"
            ET.SubElement(anime, 'my_score').text = "0"
            ET.SubElement(anime, 'my_status').text = category_name

    # Write the modified XML to the output file
    new_tree = ET.ElementTree(new_root)
    new_tree.write(output_file, encoding='utf-8', xml_declaration=True)

# Usage
input_file = 'export.xml'
output_file = 'new_export.xml'
transform_xml(input_file, output_file)

