from flask import Flask, render_template, request
import os

# app = Flask(__name__)
app = Flask(__name__, static_folder="C:\\Users\\rebecca\\Desktop\\art")

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get a list of all images in the input folder
    input_dir = 'queries'
    input_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    # If the user has submitted a form, get the selected image and its corresponding subfolder
    if request.method == 'POST':
        selected_image = request.form['image']
        sub_dir = os.path.join('results', selected_image.split('.')[0])
        # Get a list of all images in the subfolder
        sub_files = [f for f in os.listdir(sub_dir) if os.path.isfile(os.path.join(sub_dir, f))]
        # Render the template with the selected image and all images in the subfolder
        return render_template('gallery.html', selected_image=selected_image, input_files=input_files, sub_files=sub_files)
    # Otherwise, render the template with no selected image or subfolder
    return render_template('gallery.html', selected_image=None, input_files=input_files, sub_files=None)

if __name__ == '__main__':
    app.run(debug=True)
