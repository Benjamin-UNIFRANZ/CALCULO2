from PIL import Image

# Rutas del archivo original y nombres de salida
imagen_original = "./img/calculoImagen.webp"
salida_450x400 = "imagen_450x400.png"
salida_200x250 = "imagen_200x250.png"
salida_32x32 = "imagen_32x32.png"

# Función para redimensionar la imagen
def redimensionar_imagen(ruta_entrada, tamanio, ruta_salida):
    with Image.open(ruta_entrada) as img:
        img_resized = img.resize(tamanio, Image.Resampling.LANCZOS)
        img_resized.save(ruta_salida)
        print(f"Imagen guardada: {ruta_salida}, tamaño: {tamanio}")

# Crear las dos imágenes con los tamaños especificados
# redimensionar_imagen(imagen_original, (450, 400), salida_450x400)
# redimensionar_imagen(imagen_original, (200, 250), salida_200x250)
redimensionar_imagen(imagen_original, (32, 32), salida_32x32)

#pip install pillow
