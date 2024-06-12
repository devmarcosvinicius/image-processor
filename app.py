from flask import Flask, render_template, request, send_file
from PIL import Image, ImageEnhance
import io

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/brightness', methods=["POST"])
def brightness():
    file = request.files['image']
    brightness_value = float(request.form['brightness_value'])

    # Open the image file
    image = Image.open(file.stream)

    # Adjust brightness
    enhancer = ImageEnhance.Brightness(image)
    enhanced_image = enhancer.enhance(brightness_value)

    # Save the enhanced image to a BytesIO object
    img_io = io.BytesIO()
    enhanced_image.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


if __name__ == '__main__':
    app.run()
