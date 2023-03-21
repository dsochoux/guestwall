import csv
import os
import uuid
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('upload.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        name = request.form['name']
        # adding date (mm/dd/yyyy) to the end of the caption + surrounding the caption with quotes to
        # allow the caption to have commas (otherwise it will break the csv file)
        caption = "\"" + request.form['caption'] + " (" + datetime.now().strftime("%m/%d/%Y") + ")" + "\""
        image = request.files['image']
        image_id = name + str(uuid.uuid4())  # Generate a unique ID for the image. Probably overkill
        image_path = os.path.join('static', f'{image_id}.jpg')  # Construct the path to save the image
        # Save the image to the static folder
        image.save(image_path)
        # Write the data to the CSV file
        with open('data.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name, caption, image_id])
        # take the user to the wall
        return redirect(url_for('wall'))
    else:
        return render_template('upload.html')
    
@app.route('/wall')
def wall():
    visitors = []
    with open('data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            visitors.append({
                'name': row['name'],
                # the caption is stored with quotes around it to allow for commas. This is taking off the
                # leading and trailing quotes
                'caption': row['caption'].strip("\"\""),
                'imageid': row['imageid']
            })
    return render_template('wall.html', visitors=visitors)


if __name__ == '__main__':
    # only ONE app.run statment should be uncommented
    # uncomment the following line if you want access from other devices on the network (production)
    # app.run(host='0.0.0.0', port=3000)
    # uncomment the following line if you want access from only your local machine (testing)
    app.run(port=3000)