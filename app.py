from flask import Flask, render_template, request, send_file
import io
import base64
from models.Image import Image
from models.FaceDetector import FaceDetector

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/color')
def color():
    return render_template("color.html")


@app.route('/transformation')
def transformation():
    return render_template("transformation.html")


@app.route('/filter')
def filter():
    return render_template("filter.html")


@app.route('/restoration')
def restoration():
    return render_template("restoration.html")


@app.route('/face-detection')
def face_detection():
    return render_template("face-detection.html")


@app.route('/matrix')
def matrix():
    return render_template("matrix.html")


@app.route("/change_options", methods=["POST"])
def change_options():
    file = request.files['image']
    brightness_value = float(request.form['brightness_value'])
    contrast_value = float(request.form['contrast_value'])

    # Open the image file and read it using the custom Image class
    image = Image(file)

    # Adjust brightness and contrast using the custom Image class methods
    modified_image = image.change_brightness(brightness_value)
    modified_image = image.change_contrast(contrast_value)

    # Save the modified image to a BytesIO object
    img_io = io.BytesIO()
    modified_image.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


@app.route("/resize", methods=["POST"])
def resize():
    file = request.files['image']
    width_value = int(request.form["width_value"])
    height_value = int(request.form["height_value"])

    image = Image(file)

    modified_image = image.resize_image(new_height=height_value, new_width=width_value)

    img_io = io.BytesIO()
    modified_image.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


@app.route('/flip/<transform>', methods=['POST'])
def flip(transform):
    data = request.json
    image_data = base64.b64decode(data['image'].split(',')[1])

    with io.BytesIO(image_data) as file:
        image = Image(file)
        modified_image = ''

        if transform == 'original':
            modified_image = image
        elif transform == 'horizontal':
            modified_image = image.mirror_image()
        elif transform == 'vertical':
            modified_image = image.flip()
        elif transform == 'horizontal-vertical':
            pass

        image_data = io.BytesIO()
        modified_image.save(image_data, format='PNG')
        image_data.seek(0)

    return send_file(image_data, mimetype='image/png')


@app.route("/rotate1", methods=["POST"])
def rotate1():
    file = request.files['image']

    image = Image(file)

    modified_image = image.rotate_image(45)

    img_io = io.BytesIO()
    modified_image.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


@app.route("/rotate2", methods=["POST"])
def rotate2():
    file = request.files['image']

    image = Image(file)

    modified_image = image.rotate_image(90)

    img_io = io.BytesIO()
    modified_image.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


@app.route("/rotate3", methods=["POST"])
def rotate3():
    file = request.files['image']

    image = Image(file)

    modified_image = image.rotate_image(180)

    img_io = io.BytesIO()
    modified_image.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


@app.route("/rotate4", methods=["POST"])
def rotate4():
    file = request.files['image']

    image = Image(file)

    modified_image = image.rotate_image(360)

    img_io = io.BytesIO()
    modified_image.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


@app.route("/smoothing", methods=["POST"])
def smoothing():
    file = request.files['image']

    image = Image(file)

    modified_image = image.smooth_image()

    img_io = io.BytesIO()
    modified_image.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


@app.route("/restoration", methods=["POST"])
def reconstruction():
    file = request.files['image']

    image = Image(file)

    modified_image = image.sharpen_image()

    img_io = io.BytesIO()
    modified_image.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


@app.route("/face_detector", methods=["POST"])
def face_detector():
    file = request.files['image']

    face_detector = FaceDetector("image", file)

    modified_image = face_detector.run()

    img_io = io.BytesIO()
    modified_image.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


@app.route("/get_matrix", methods=["POST"])
def get_matrix():
    file = request.files['image']
    image = Image(file)
    excel_buffer = image.write_image_in_excel()

    # Retornar o arquivo Excel como uma resposta HTTP
    return send_file(
        excel_buffer,
        as_attachment=True,
        download_name='image_matrix.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


if __name__ == '__main__':
    app.run(debug=True)
