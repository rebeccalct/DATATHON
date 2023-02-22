import matplotlib.pyplot as plt
import pandas as pd
import numpy
import os
import requests
from PIL import Image
import io
import csv

os.chdir("C:\\Users\\rebecca\\desktop\\filescsv")
def display_artwork(url):
    response = requests.get(url)
    image = Image.open(io.BytesIO(response.content))
    plt.imshow(image)
    plt.axis("off")
    plt.show()


artist = pd.read_csv("Artist.csv") # 616 artist
artist.columns
artistspe = pd.read_csv("ArtistSpecializations.csv") # 376 rows, (not 616 because many artist no specialization)
artistspe.columns 
artistspe["artist_id"].value_counts()
artistspe["artist_id"].nunique() # 234 people, so it means some artist can belong to several specifications

spe = pd.read_csv("specialization.csv")
asp = pd.merge(artistspe, spe, left_on='specialty_id', right_on='id',how='inner')
asp2 = pd.DataFrame(asp["name"].value_counts())
asp2 = asp2.rename(columns={"name":"value"})
asp2  # sort specilizations

# be influenced (student and teacher)
apprenticeship = pd.read_csv("Apprenticeship.csv") 

# discuss the artwork list and their similarity
import io
import matplotlib.pyplot as plt
import requests
from PIL import Image

artwork  = pd.read_csv("Artwork.csv",encoding = "ISO-8859-1") # 10517 pictures
artwork.columns
artwork["artist"].nunique() # 610 artist

display_artwork(artwork.image_url.values[0])


# Define the path to the CSV file
csv_file_path = "C:\\Users\\rebecca\\desktop\\filescsv\\Artwork.csv"

# Define the path to the directory where the images will be saved
output_dir = "E:\\datathon\\images"
os.makedirs(output_dir, exist_ok=True)

with open(csv_file_path, "r",encoding = "ISO-8859-1") as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # Skip the header row
    for row in reader:
        try:
            image_url = row[3]  
            response = requests.get(image_url)
            image_name = os.path.basename(image_url)
            new_name = row[0]+ "+" + image_name
            output_path = os.path.join(output_dir, new_name)
            with open(output_path, "wb") as f:
                f.write(response.content)
                print(f"Downloaded {image_name}")
        except:
            pass 

# file name of pictures
new_col = []
index = pd.read_csv("index.csv",header=None)
for link in index.iloc[:,[0]].values:
    new = link[0].replace("E:\\datathon\\images\\","")
    new_col.append(new)

index.iloc[:,[0]] = new_col
index.to_csv("index2.csv")














