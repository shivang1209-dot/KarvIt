from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# Endpoint to create disk image
'''

Body-data : {"driveName": "E:"}

'''

@app.route('/disk-image', methods=['POST'])
def create_disk_image():
    data = request.json
    drive_name = data.get('driveName')
    if not drive_name:
        return jsonify({'error': 'Drive name is required'}), 400

    try:
        # Call your existing script to create a disk image
        result = subprocess.run(['python', 'python/disk_imager.py', '--create-image', drive_name], capture_output=True, text=True)
        return jsonify({'message': 'Disk image created successfully', 'output': result.stdout}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to carve files from a disk image
'''

Body data :
{
  "imagePath": "/path/to/disk/image",
  "fileType": "png"
}

'''

@app.route('/carve-file', methods=['POST'])
def carve_file():
    data = request.json
    image_path = data.get('imagePath')
    file_type = data.get('fileType')
    
    if not image_path or not file_type:
        return jsonify({'error': 'Image path and file type are required'}), 400

    try:
        # Call your existing script to carve files
        result = subprocess.run(['python', 'python/file_carver.py', '--file', image_path, '--type', file_type], capture_output=True, text=True)
        return jsonify({'message': 'File carving completed', 'output': result.stdout}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
