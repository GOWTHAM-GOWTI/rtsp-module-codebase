from flask import Flask, render_template, Response, request
import cv2 as cv
import pymongo

from utils.common import gen_frames

app = Flask(__name__)

client = pymongo.MongoClient('mongodb://root:root@mongo:27017/')
db = client.rtsp

@app.route('/', methods=["GET","POST"])
def home():
    if request.method=="POST":
        items=request.form.get("input") 
        total_items_requested = int(items)
        items= [x for x in range(0, total_items_requested)]

        # Set / store search counter in mongo
        db['config'].update({'type': 'search'}, {'$set': {'value': total_items_requested}}, upsert=True)

        return render_template("index.html", items=items)

    search_items = db['config'].find_one({'type': 'search'})
    total_cams = 1
    if search_items:
        total_cams = search_items.get('value', 1)
    
    items= [x for x in range(total_cams)]
    
    return render_template("index.html", items=items)

@app.route('/video_feed')
def video_feed():
    vcap = cv.VideoCapture("./yolo/traffic.mp4")
    
    # Return frames of the stream one by one
    return Response(gen_frames(vcap), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)