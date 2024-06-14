document.getElementById('image').addEventListener('change', function () {
    const fileInput = document.getElementById('image');
    if (fileInput.files.length > 0) {
        // Hide the upload div
        document.getElementById('upload').style.display = 'none';

        // Display the uploaded image in canvas
        const file = fileInput.files[0];
        const reader = new FileReader();
        reader.onload = function (e) {
            const img = new Image();
            img.onload = function () {
                const canvas = document.getElementById('canvas');
                const ctx = canvas.getContext('2d');

                // Set canvas size to match the image
                canvas.width = img.width;
                canvas.height = img.height;

                // Draw image onto the canvas
                ctx.drawImage(img, 0, 0);
            }
            img.src = e.target.result;
        }
        reader.readAsDataURL(file);
    } else {
        alert('Por favor, selecione uma imagem primeiro.');
    }
});

function applyColorsManipulation(event) {
    event.preventDefault();
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const fileInput = document.getElementById('image');
    const brightnessRange = document.getElementById('brightness').value;
    const contrastRange = document.getElementById('contrast').value;

    if (fileInput.files.length === 0) {
        alert('Por favor, carregue uma imagem primeiro.');
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('image', file);
    formData.append('brightness_value', brightnessRange);
    formData.append('contrast_value', contrastRange);

    fetch('/change_options', {
        method: 'POST',
        body: formData
    })
        .then(response => response.blob())
        .then(blob => {
            const url = URL.createObjectURL(blob);
            const img = new Image();
            img.onload = function () {
                // Adjust canvas size
                canvas.width = img.width;
                canvas.height = img.height;
                // Draw the updated image onto the canvas
                ctx.drawImage(img, 0, 0);
                URL.revokeObjectURL(url);
            }
            img.src = url;
        })
        .catch(error => console.error('Erro ao aplicar brilho e contraste:', error));
}

function applyResize(event) {
    event.preventDefault();
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const fileInput = document.getElementById('image');
    const heightValue = document.getElementById('height').value;
    const widthValue = document.getElementById('width').value;

    if (fileInput.files.length === 0) {
        alert('Por favor, carregue uma imagem primeiro.');
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('image', file);
    formData.append('height_value', heightValue);
    formData.append('width_value', widthValue);

    fetch('/resize', {
        method: 'POST',
        body: formData
    })
        .then(response => response.blob())
        .then(blob => {
            const url = URL.createObjectURL(blob);
            const img = new Image();
            img.onload = function () {
                // Adjust canvas size
                canvas.width = img.width;
                canvas.height = img.height;
                // Draw the updated image onto the canvas
                ctx.drawImage(img, 0, 0);
                URL.revokeObjectURL(url);
            }
            img.src = url;
        })
        .catch(error => console.error('Erro ao aplicar o resize:', error));
}

function applyFlip(transform) {
    const canvas = document.getElementById('canvas');
    const imageData = canvas.toDataURL();

    fetch(`/flip/${transform}`, {
        method: 'POST',
        body: JSON.stringify({ image: imageData }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.blob())
    .then(blob => {
        const imageUrl = URL.createObjectURL(blob);
        const img = new Image();
        img.onload = function () {
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');
            // Set canvas size to match the image
            canvas.width = img.width;
            canvas.height = img.height;
            // Draw the updated image onto the canvas
            ctx.drawImage(img, 0, 0);
            URL.revokeObjectURL(imageUrl);
        }
        img.src = imageUrl;
    })
    .catch(error => console.error('Erro:', error));
}
