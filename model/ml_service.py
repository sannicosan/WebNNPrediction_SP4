import json
import os
import time

import numpy as np
import redis
import settings
from tensorflow.keras.applications import resnet50
from tensorflow.keras.applications.resnet50 import decode_predictions, preprocess_input, ResNet50
from tensorflow.keras.preprocessing import image

# [DONE]
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
                host = settings.REDIS_IP ,
                port = settings.REDIS_PORT,
                db = settings.REDIS_DB_ID
                )

# [DONE]
# Load your ML model and assign to variable `model`
# See https://drive.google.com/file/d/1ADuBSE4z2ZVIdn66YDSwxKv-58U7WEOn/view?usp=sharing
# for more information about how to use this model.
model = ResNet50()


def predict(image_name):
    """
    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.

    Parameters
    ----------
    image_name : str
        Image filename.

    Returns
    -------
    class_name, pred_probability : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    # [DONE]
    # Load image from \uploads
    img = image.load_img(os.path.join(settings.UPLOAD_FOLDER,image_name),target_size=(224, 224)) 
    
    # Image preprocessing
    x= image.img_to_array(img)
    x_batch = np.expand_dims(x, axis = 0)
    x_batch = resnet50.preprocess_input(x_batch)
    
    # Image prediction & Output
    try:
        img_pred = model.predict(x_batch)
        _, class_name, pred_probability = resnet50.decode_predictions(img_pred, top = 1)[0][0]
    except:
        class_name, pred_probability = 'BottleNeck', 0    
    
    return class_name, np.round(pred_probability,4)


def classify_process():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.

    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.
    """
    while True:
        # [DONE]
        # Inside this loop you should add the code to:
        #   1. Take a new job from Redis
        #   2. Run your ML model on the given data
        #   3. Store model prediction in a dict with the following shape:
        #      {
        #         "prediction": str,
        #         "score": float,
        #      }
        #   4. Store the results on Redis using the original job ID as the key
        #      so the API can match the results it gets to the original job
        #      sent
        # Hint: You should be able to successfully implement the communication
        #       code with Redis making use of functions `brpop()` and `set()`.
        
        # Read the job from Redis
        _ , msg= db.brpop(settings.REDIS_QUEUE)                                 # queue_name, msg <- 
        # print(f'Message from user: {msg}')
        
        # Decode image_name
        msg_dict = json.loads(msg)
        img_name = msg_dict['image_name']
        job_id =  msg_dict['id']
        
        # Predict
        pred_class, pred_proba = predict(img_name)
        pred_dict = {
                    "prediction": pred_class,
                    "score": np.round(float(pred_proba),4),
                    }
        
        db.set(job_id,json.dumps(pred_dict))

        # Don't forget to sleep for a bit at the end
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()
