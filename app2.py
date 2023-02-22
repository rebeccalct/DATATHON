import os
import base64
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

os.environ.get('PYTHONPATH')
# Set the input and output folder paths
input_folder = 'queries'
output_folder = 'results'

# Define the app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    dcc.Dropdown(
        id='image-dropdown',
        options=[{'label': name, 'value': name} for name in os.listdir(input_folder)],
        placeholder='Select an image'
    ),
    html.Div(id='output-images')
])


# Define a function to load images from a folder
def load_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            img_path = os.path.join(folder_path, filename)
            with open(img_path, 'rb') as f:
                encoded_image = base64.b64encode(f.read()).decode('utf-8')
                images.append(html.Img(src='data:image/png;base64,{}'.format(encoded_image)))
    return images


# Define a callback to update the output images
@app.callback(Output('output-images', 'children'),
            [Input('image-dropdown', 'value')])


def update_output(value):
    # div_width = "%"
    if value is not None:
        # Get the input and output folder paths
        input_path = os.path.join(input_folder, value)
        output_path = os.path.join(output_folder, os.path.splitext(value)[0])

        # Load the selected image and display it
        with open(input_path, 'rb') as f:
            encoded_image = base64.b64encode(f.read()).decode('utf-8')
            image = html.Img(src='data:image/png;base64,{}'.format(encoded_image))

        # Load the images in the corresponding subfolder and display them
        images= load_images_from_folder(output_path)

        return html.Div([
            image,
            html.Hr(),
            # html.H3('Images in {}'.format(output_path)),
            # html.H3(names),
            html.H3('Output: Similar pictures'),
            # html.Div(images,style={"width": div_width})
            html.Div(images)
        ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)