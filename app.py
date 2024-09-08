from flask import Flask, request, render_template
import os
from image_processing import compare_images  # Import the image processing function

app = Flask(__name__)

UPLOAD_FOLDER = 'static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get uploaded files
        original_file = request.files['original']
        altered_file = request.files['altered']

        # Define file paths
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], 'original.jpg')
        altered_path = os.path.join(app.config['UPLOAD_FOLDER'], 'altered.jpg')

        # Save uploaded files to the static folder
        original_file.save(original_path)
        altered_file.save(altered_path)

        # Compare images using the processing function
        are_identical = compare_images(original_path, altered_path)

        # Set the result message
        if are_identical:
            result_message = "The images are identical."
        else:
            result_message = "The images are different."

        # Render the result page
        return render_template('result.html', result=result_message)

    # Render the index page (file upload form)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
