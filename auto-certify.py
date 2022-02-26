import csv
from PIL import Image, ImageDraw, ImageFont
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


# Configurations
FONT_FILE = ImageFont.truetype(r'GreatVibes-Regular.ttf', 250)
FONT_COLOR = '#1883db'
WIDTH, HEIGHT = 2916.5, 1800
G_FOLDER = 'FOLDER ID' # https://drive.google.com/drive/folders/"Folder ID"
# Names should be in file: names.csv (Without Headers)
# Certificate should be in file: Certificate.png
# client_secrets.json is required for Google Drive API


# Google Drive Authentication
gauth = GoogleAuth()           
drive = GoogleDrive(gauth)
gauth.LocalWebserverAuth()


# Functions
def make_cert(name):
    """Function to generate certificate"""
    image_source = Image.open(r'Certificate.png')
    draw = ImageDraw.Draw(image_source)
    name_width, name_height = draw.textsize(name, font=FONT_FILE)
    draw.text((WIDTH-name_width/2, HEIGHT-name_height/2), name, fill=FONT_COLOR, font=FONT_FILE)
    image_source.save('Exports\\' + name.strip() + '.png')
    print('Making certificate of: ' + name.strip())

def get_names():
    """Function to get names list from file"""
    names_file = open(r'names.csv', 'r')
    reader = csv.reader(names_file)
    names = []
    for row in reader:
        if len(row) != 0:
            names.append(row[0])

    return names

def upload(name):
    """Function to upload certificate to Google Drive"""
    global G_FOLDER

    file_name = 'Exports\\' + name.strip() + '.png'
    gfile = drive.CreateFile({'parents': [{'id': G_FOLDER}]})
    gfile.SetContentFile(file_name)
    gfile['title'] = name.strip()
    gfile.Upload()
    print('Uploaded certificate')

    file_id = gfile['id']
    link = f'https://drive.google.com/file/d/{file_id}/view'
    return link


# Main Script
names = get_names()

names_file = open(r'names.csv', 'w', newline='')
writer = csv.writer(names_file)

for name in names:
    make_cert(name)
    link = upload(name)
    writer.writerow([name, link])

names_file.close()
print('Done!')