import os
from flask import Flask, render_template, request, send_file
import xml.etree.ElementTree as ET
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['OUTPUT_FOLDER'] = os.path.join(os.getcwd(), 'outputs')

# Ensure upload and output folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


def transform_xml(input_file, output_file):
    # Parse the input XML
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Create the new root structure
    new_root = ET.Element('myanimelist')

    # Copy myinfo section if it exists
    myinfo = root.find('myinfo')
    if myinfo is not None:
        new_myinfo = ET.SubElement(new_root, 'myinfo')
        new_myinfo.extend(myinfo)  # Copy all child elements

    # Process each anime entry
    for anime in root.findall('anime'):
        # Create new anime element
        new_anime = ET.SubElement(new_root, 'anime')
        
        # Copy existing fields
        for child in anime:
            # Create a new element with the same tag and text
            new_child = ET.SubElement(new_anime, child.tag)
            new_child.text = child.text

        # Add additional fields if they don't exist (customize as needed)
        if anime.find('my_watched_episodes') is None:
            ET.SubElement(new_anime, 'my_watched_episodes').text = "0"
        if anime.find('my_start_date') is None:
            ET.SubElement(new_anime, 'my_start_date').text = "0000-00-00"
        if anime.find('my_finish_date') is None:
            ET.SubElement(new_anime, 'my_finish_date').text = "0000-00-00"
        if anime.find('my_score') is None:
            ET.SubElement(new_anime, 'my_score').text = "0"

    # Write the modified XML to the output file with proper formatting
    new_tree = ET.ElementTree(new_root)
    ET.indent(new_tree, space="  ")  # Add indentation for readability
    new_tree.write(output_file, encoding='utf-8', xml_declaration=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file:
            filename = secure_filename(file.filename)
            input_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            output_file = os.path.join(app.config['OUTPUT_FOLDER'], 'new_export.xml')

            # Save the uploaded file
            file.save(input_file)

            # Transform the XML
            transform_xml(input_file, output_file)

            # Serve the transformed file
            return send_file(output_file, as_attachment=True, download_name='new_export.xml')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)
