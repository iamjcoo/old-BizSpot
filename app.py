from flask import Flask, render_template, json, jsonify, request, redirect, send_file
import numpy as np
import cv2
from base64 import b64decode


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('app.html')

@app.route("/analyze", methods=['GET','POST'])
def analyze():
    file = request.form['img']
    thresh = int(request.form['thresh'])
    header, encoded = file.split(",", 1)
    data = b64decode(encoded)
    nparr = np.fromstring(data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)

    count = 0.0
    area = 0.0

    # get image properties.
    h, w, bpp = np.shape(img)


    for py in range(0, h):
        for px in range(0, w):
            if img[py][px][0] >= thresh:
                    img[py][px][:]=255
                    count = count + 1
            else:
                    img[py][px][:] = 0

    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    edged = cv2.Canny(blurred, 0, 50)
    cnts, hierarchy = cv2.findContours(edged,
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    #cv2.drawContours(img, cnts, -1, (0, 255, 0), 3)

    for i in range(0, len(cnts)):
        #print(cv2.contourArea(cnts[i]))
        if(cv2.contourArea(cnts[i])>50):
            cv2.drawContours(img, cnts[i], -1, (0, 255, 0), 3)
        area = area + cv2.contourArea(cnts[i])

    return str(round((count / (h*w))*100, 2))

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
