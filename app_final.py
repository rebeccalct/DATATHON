from jupyter_dash import JupyterDash
import dash_cytoscape as cyto
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import numpy as np
# from geopy.geocoders import Nominatim
import folium
import base64
import pandas as pd
import requests
import warnings
import pandas as pd
from urllib.request import urlopen
from base64 import b64encode
import os
import dash
from dash.dependencies import Input, Output, State

warnings.filterwarnings("ignore")
artworks_country = pd.read_csv("https://github.com/Themaoyc/datathon2023/blob/master/map1.csv?raw=true")
artworks_country['new_description'] = artworks_country['name'].str.replace(' ', '%20')
url_prefix = 'https://github.com/Themaoyc/datathon2023/blob/master/famous%20painting/'
artworks_country['url'] = artworks_country['new_description'].apply(lambda x: url_prefix + x +'.jpg')
m = folium.Map(location=[45.5236, -122.6750], zoom_start=2)
def get_country_location(country):
    url = 'https://nominatim.openstreetmap.org/search?q={}&format=json&limit=1'.format(country)
    response = requests.get(url).json()
    if response:
        return [response[0]['lat'], response[0]['lon']]
    else:
        return None
for _, row in artworks_country.iterrows():
    painter_image_url = row['url']
    country = row['country']
    introduction = row['summary']
    painter_image_url += '?raw=true'
    painter_image_content = requests.get(painter_image_url).content
    painter_encoded_image = base64.b64encode(painter_image_content).decode('utf-8')
    
    painter_image_url += '?raw=true'
    html_str = '<img src="{}" width="200" height="200">'.format(painter_image_url)
    html_str += '<br><b>Introduction:</b><br>'+introduction

    # 创建包含HTML字符串的IFrame和Popup
    iframe = folium.IFrame(html=html_str, width=500, height=500)
    popup = folium.Popup(iframe, max_width=500)
    # 将包含Popup的标记添加到对应的国家
    folium.Marker(location=get_country_location(country),
                  icon=folium.Icon(color='green', icon='info-sign'),
                  popup=popup).add_to(m)
m

os.environ.get('PYTHONPATH')
# Set the input and output folder paths
input_folder = 'C:\\Users\\rebecca\\Desktop\\art\\queries'
output_folder = 'C:\\Users\\rebecca\\Desktop\\art\\results'
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

df_selected = pd.read_csv('https://raw.githubusercontent.com/LiuYinFu6/datathon/main/Myselected.csv')
df_movement = pd.read_csv('https://raw.githubusercontent.com/LiuYinFu6/datathon/main/Movement.csv')
df_generated = pd.read_csv('https://raw.githubusercontent.com/LiuYinFu6/datathon/main/Generated.csv')
# 获取所有图像的URL
image_urls = df_selected['image_url'].tolist()

external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]
app = JupyterDash(__name__)
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

app.layout = html.Div([html.H1('Datathon 2023', style={'textAlign': 'center'}),
    html.H3('Group LGMZU', style={'textAlign': 'center'}),
###加上后续的介绍！
    html.Img(src='https://github.com/Themaoyc/datathon2023/blob/master/map1.jpg?raw=true', 
              style={'display': 'block', 'margin': 'auto', 'width': '20%'}),
dcc.Tabs(id="tabs-inline", value='tab-1', parent_className='custom-tabs', className='custom-tabs-container',
             children=[
                 dcc.Tab(label='Map', value='Map', style=tab_style, selected_style=tab_selected_style),
                 dcc.Tab(label='Similar Images Generator', value='Similar Images Generator', style=tab_style,
                         selected_style=tab_selected_style),
                 dcc.Tab(label='AI picture generator', value='AI picture generator', style=tab_style,
                         selected_style=tab_selected_style),
                 
             ], style=tabs_styles),
html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              Input('tabs-inline', 'value'))

def render_content(tab):
    if tab == 'Map':
        return html.Div([
    html.H1('Interactive Map'),
    # 将地图嵌入 Dash 应用程序
    html.Iframe(id='folium-map', srcDoc=m._repr_html_(), width='100%', height='600'),
])

    elif tab == 'Similar Images Generator':
        return html.Div([
    dcc.Dropdown(
    id='image-dropdown',
        options=[{'label': name, 'value': name} for name in os.listdir(input_folder)],
        placeholder='Select an image'
    ),
    html.Div(id='output-images')
])

    elif tab == 'AI picture generator':
        return html.Div([
    html.Div([
        html.H2('Select an image'),
        html.Div([
            html.Img(src=url, style={'height': '300px'}) for url in image_urls
        ]),
        dcc.RadioItems(
            id='image-radio',
            options=[{'label': url, 'value': url} for url in image_urls],
            labelStyle={'display': 'block'}
        )
    ]),
    html.Div([
        html.H2('Select a name'),
        dcc.Dropdown(
            id='name-dropdown',
            options=[{'label': name, 'value': name} for name in df_movement['name'].unique()]
        )
    ]),
    html.Button('Submit', id='submit-button'),
    html.Div([
        html.H2('Generated Image'),
        html.Img(id='generated-image')
    ])
])

    
# 回调函数1：更新图像
@app.callback(Output('selected-image', 'src'),
              [Input('image-radio', 'value')])
def update_image(image_url):
    return image_url

# 回调函数2：保存选择的名字
@app.callback(Output('name-selection', 'children'),
              [Input('name-dropdown', 'value')])
def save_name(name):
    return name

# 回调函数3：随机显示一个生成的图像
@app.callback(Output('generated-image', 'src'),
              [Input('submit-button', 'n_clicks')],
              [State('image-radio', 'value'),
               State('name-dropdown', 'value')])
def update_generated_image(n_clicks, selected_image, selected_name):
    if n_clicks:
        # 获取所有与所选名称匹配的行
        df_matching_names = df_movement.loc[df_movement['name'] == selected_name]
        # 从匹配行中随机选择一行
        selected_row = df_matching_names.sample()
        # 获取选择行的图像URL
        generated_url = df_generated.loc[selected_row.index[0], 'image_url']
        return generated_url
    return None

# Define a callback to update the output images
@app.callback(Output('output-images', 'children'),
            [Input('image-dropdown', 'value')])
            
def update_output(value):
     if value is not None:
        # Get the input and output folder paths
        input_path = os.path.join(input_folder, value)
        output_path = os.path.join(output_folder, os.path.splitext(value)[0])

        # Load the selected image and display it
        with open(input_path, 'rb') as f:
            encoded_image = base64.b64encode(f.read()).decode('utf-8')
            image = html.Img(src='data:image/png;base64,{}'.format(encoded_image))

        # Load the images in the corresponding subfolder and display them
        images = load_images_from_folder(output_path)

        return html.Div([
            image,
            html.Hr(),
            html.H3('OUTPUT similar images'),
            html.Div(images)
        ])

# Run the app
if __name__ == '__main__':
     app.run_server(debug=True, threaded=True,dev_tools_ui=False,dev_tools_props_check=False,port=1000)
