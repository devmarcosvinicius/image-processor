document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.main__image-container').style.display = 'none';
    document.querySelector('.downloadImage').style.display = 'none';
});

document.getElementById('image').addEventListener('change', function () {
    const fileInput = document.getElementById('image');
    if (fileInput.files.length > 0) {
        // Esconde o div de upload
        document.getElementById('upload').style.display = 'none';

        // Mostra os containers e o botão de download
        document.querySelector('.main__image-container').style.display = 'flex';
        document.querySelector('.downloadImage').style.display = 'block';

        // Exibe a imagem carregada no canvas
        const file = fileInput.files[0];
        const reader = new FileReader();
        reader.onload = function (e) {
            const img = new Image();
            img.onload = function () {
                const canvas = document.getElementById('canvas');
                const ctx = canvas.getContext('2d');

                // Ajusta o tamanho do canvas para corresponder à imagem
                canvas.width = img.width;
                canvas.height = img.height;

                // Desenha a imagem no canvas
                ctx.drawImage(img, 0, 0);
            }
            img.src = e.target.result;
        }
        reader.readAsDataURL(file);
    } else {
        alert('Por favor, selecione uma imagem primeiro.');
    }
});

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

document.getElementById('webcam').addEventListener('click', function () {
    // Verifica se o navegador suporta acesso à webcam
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        // Solicita acesso à webcam
        navigator.mediaDevices.getUserMedia({video: true})
            .then(function (stream) {
                // Sucesso! O usuário concedeu acesso à webcam
                console.log('Acesso à webcam concedido');
                // Define o stream como a fonte do elemento de vídeo
                var video = document.getElementById('video');
                video.srcObject = stream;
            })
            .catch(function (error) {
                // O usuário negou o acesso ou ocorreu um erro
                console.error('Erro ao acessar a webcam:', error);
            });
    } else {
        console.error('Seu navegador não suporta acesso à webcam');
    }
});

function downloadImage() {
    const canvas = document.getElementById('canvas');
    const link = document.createElement('a');
    link.href = canvas.toDataURL('image/png');
    link.download = 'image.png';
    link.click();
}

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
        body: JSON.stringify({image: imageData}),
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

function sendImageForFaceDetection() {
    const fileInput = document.getElementById('image');
    if (fileInput.files.length === 0) {
        alert('Por favor, carregue uma imagem primeiro.');
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('image', file);

    fetch('/face_detector', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        const url = URL.createObjectURL(blob);
        const img = new Image();
        img.onload = function () {
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');

            // Set canvas size to match the image
            canvas.width = img.width;
            canvas.height = img.height;

            // Draw the updated image onto the canvas
            ctx.drawImage(img, 0, 0);
            URL.revokeObjectURL(url);
        }
        img.src = url;
    })
    .catch(error => console.error('Erro ao aplicar a detecção facial:', error));
}

function applyRotation1() {
    const imageFile = document.getElementById('image').files[0];
    if (!imageFile) {
        alert('Por favor, carregue uma imagem primeiro.');
        return;
    }

    const formData = new FormData();
    formData.append('image', imageFile);

    fetch('/rotate1', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        const imageUrl = URL.createObjectURL(blob);
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        img.onload = function() {
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);
        }
        img.src = imageUrl;
    })
    .catch(error => console.error('Erro ao aplicar a rotação:', error));
}

function applyRotation2() {
    const imageFile = document.getElementById('image').files[0];
    if (!imageFile) {
        alert('Por favor, carregue uma imagem primeiro.');
        return;
    }

    const formData = new FormData();
    formData.append('image', imageFile);

    fetch('/rotate2', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        const imageUrl = URL.createObjectURL(blob);
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        img.onload = function() {
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);
        }
        img.src = imageUrl;
    })
    .catch(error => console.error('Erro ao aplicar a rotação:', error));
}

function applyRotation3() {
    const imageFile = document.getElementById('image').files[0];
    if (!imageFile) {
        alert('Por favor, carregue uma imagem primeiro.');
        return;
    }

    const formData = new FormData();
    formData.append('image', imageFile);

    fetch('/rotate3', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        const imageUrl = URL.createObjectURL(blob);
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        img.onload = function() {
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);
        }
        img.src = imageUrl;
    })
    .catch(error => console.error('Erro ao aplicar a rotação:', error));
}

function applyRotation4() {
    const imageFile = document.getElementById('image').files[0];
    if (!imageFile) {
        alert('Por favor, carregue uma imagem primeiro.');
        return;
    }

    const formData = new FormData();
    formData.append('image', imageFile);

    fetch('/rotate4', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        const imageUrl = URL.createObjectURL(blob);
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        img.onload = function() {
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);
        }
        img.src = imageUrl;
    })
    .catch(error => console.error('Erro ao aplicar a rotação:', error));
}

function downloadMatrix() {
    fetch('/get_matrix', {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao gerar a matriz.');
        }
        return response.blob();
    })
    .then(blob => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'matrix.xlsx';  // Nome do arquivo que será baixado
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Ocorreu um erro ao gerar a matriz.');
    });
}