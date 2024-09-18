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

    # Convert folder data from original XML to new format
    for folder in root.findall('folder'):
        category_name = folder.find('name').text
        if category_name == "Plan to watch":
            category_name = "Plan to Watch"
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        # Handle file upload
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file.filename != "export.xml":
            return "Invalid file name"
        if file:
            filename = secure_filename(file.filename)
            input_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            output_file = os.path.join(app.config['OUTPUT_FOLDER'], 'new_export.xml')  # Fixed output filename

            # Save the uploaded file
            file.save(input_file)

            # Transform the XML
            transform_xml(input_file, output_file)

            # Serve the transformed file with the fixed name 'new_export.xml'
            return send_file(output_file, as_attachment=True, download_name='new_export.xml')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)

