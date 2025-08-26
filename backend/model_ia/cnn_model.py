import tensorflow as tf
import numpy as np
from PIL import Image, ImageStat


model = tf.keras.models.load_model('backend/model_ia/model_vgg16.h5') 


def load_and_predict(image_path):

    if not image_path.lower().endswith(".jpg") and not image_path.lower().endswith(".jpeg"):
        return "Solo se permiten imágenes en formato JPG."

    try:
        
        image = Image.open(image_path)
        image = image.resize((224, 224))  
        image = np.array(image) / 255.0  
        image = np.expand_dims(image, axis=0)  

        
        prediction = model.predict(image)

        
        if prediction[0][0] > 0.5:
            return 'MALIGNO'
        elif prediction[0][0] <= 0.5:
            return 'BENIGNO'
        else:
            return 'desconocido'

    except Exception as e:
        return f"Error al procesar la imagen: {e}"
    
    
    