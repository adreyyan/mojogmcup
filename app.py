from flask import Flask, render_template, request, send_from_directory
import os
from werkzeug.utils import secure_filename
from image_processing.processor import add_gm_cup

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'nft_uploads')
PROCESSED_FOLDER = os.path.join(app.root_path, 'static', 'nft_processed')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['nft_image']
        creature = request.form['creature']
        gender = request.form['gender']
        skin_tone = request.form.get('skin_tone', '1')  # Default to '1' if not provided

        if not file or file.filename == '':
            return 'No selected file', 400

        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            if creature == 'human':
                gm_cup_filename = f"{gender}_tone{skin_tone}.png"
                gm_cup_folder = os.path.join(creature, gender)
            else:
                # For 'demon' and 'spirit', use only the tone1.png without gender in the filename
                gm_cup_filename = f"{gender}_tone1.png"
                gm_cup_folder = creature
            
            gm_cup_path = os.path.join(app.root_path, 'static', 'assets', 'gm_cups', gm_cup_folder, gm_cup_filename)

            result_image_path = add_gm_cup(file_path, gm_cup_path, PROCESSED_FOLDER)

            return send_from_directory(PROCESSED_FOLDER, os.path.basename(result_image_path))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
