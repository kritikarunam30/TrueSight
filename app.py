from flask import Flask, render_template, url_for, redirect, request, send_from_directory
#from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import SubmitField

# Setup app and sql
app = Flask(__name__)
app.config["SECRET_KEY"] = "akdndjenvkd"
app.config["UPLOADED_PHOTOS_DEST"] = "uploads"

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

class UploadForm(FlaskForm):
    photo = FileField(
        validators= [
            FileAllowed(photos, "Only images are allowed"),
            FileRequired("File Field should not be empty")
        ]
    )
    submit = SubmitField("Upload")

@app.route("/uploads/<filename>")
def get_file(filename):
    return send_from_directory(app.config["UPLOADED_PHOTOS_DEST"], filename)

@app.route('/')
def index():
    # Redirect User to First Page
    return render_template("index.html")

#@app.route is a decorator
@app.route("/detect", methods=["POST", "GET"])
def detect():
    # Redirect User to Detect Page    
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for("get_file", filename=filename)
    
    else:
        file_url = None

    return render_template("detect.html", form=form, file_url=file_url)

@app.route("/info")
def info():
    # Redirect user to info page
    return render_template("info.html")


if __name__ == "__main__":
    app.run(debug=True)