import json
import os
import re
import settings
import utils
import ast 
from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from middleware import model_predict

router = Blueprint("app_router", __name__, template_folder="templates")


@router.route("/", methods=["GET", "POST"])
def index():
    """
    GET: Index endpoint, renders our HTML code.

    POST: Used in our frontend so we can upload and show an image.
    When it receives an image from the UI, it also calls our ML model to
    get and display the predictions.
    """
    
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        # No file received, show basic UI
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        # File received but no filename is provided, show basic UI
        file = request.files["file"]
        if file.filename == "":
            flash("No image selected for uploading")
            return redirect(request.url)

        # File received and it's an image, we must show it and get predictions
        if file and utils.allowed_file(file.filename):
            # In order to correctly display the image in the UI and get model
            # predictions you should implement the following:
            #   1. Get an unique file name using utils.get_file_hash() function
            #   2. Store the image to disk using the new name
            #   3. Send the file to be processed by the `model` service
            #      Hint: Use middleware.model_predict() for sending jobs to model
            #            service using Redis.
            #   4. Update `context` dict with the corresponding values
            
            # print('IMAGE LOADING...')
            # 1. Creates unique name
            img_name = utils.get_file_hash(file)
            img_path = os.path.join(settings.UPLOAD_FOLDER,img_name)
            # 2. Stores image in '\upload'
            file.save(img_path)
            file.close()
            
            # 3. Sents image to be processed by the ML model
            prediction, score = model_predict(img_name)
            
            # 4. Updates context
            context = {
                    "prediction": prediction,
                    "score": score,
                    "filename": img_path                      
                    }
            
            # [DONE] Update `render_template()` parameters as needed 
            return render_template("index.html", filename=img_name, context=context)
        # File received and but it isn't an image
        else:
            flash("Allowed image types are -> png, jpg, jpeg, gif")
            return redirect(request.url)


@router.route("/display/<filename>")
def display_image(filename):
    """
    Display uploaded image in our UI.
    """
    return redirect(url_for("static", filename="uploads/" + filename), code=301)


@router.route("/predict", methods=["GET", "POST"])
def predict(file = None):
    """
    Endpoint used to get predictions without need to access the UI.

    Parameters
    ----------
    file : str
        Input image we want to get predictions from.

    Returns
    -------
    flask.Response
        JSON response from our API having the following format:
            {
                "success": bool,
                "prediction": str,
                "score": float,
            }

        - "success" will be True if the input file is valid and we get a
          prediction from our ML model.
        - "prediction" model predicted class as string.
        - "score" model confidence score for the predicted class as float.
    """
    # [DONE] To correctly implement this endpoint you should:
    #   1. Check a file was sent and that file is an image
    #   2. Store the image to disk
    #   3. Send the file to be processed by the `model` service
    #      Hint: Use middleware.model_predict() for sending jobs to model
    #            service using Redis.
    #   4. Update and return `rpse` dict with the corresponding values
    # If user sends an invalid request (e.g. no file provided) this endpoint
    # should return `rpse` dict with default values HTTP 400 Bad Request code
    
    response_data = {"success": False, "prediction": None, "score": None} 
    status_code = 400
     
    if request.method == "GET":  
        status_code = 405
        # return current_app.response_class(status = 405, mimetype = 'application/json')
        
    elif request.method == "POST":
        
        # Check for file received 
        if "file" in request.files: file = request.files['file']
        #  # No file received, show basic UI
        # if "file" not in request.files:
        #     status_code = 400
        #     # return current_app.response_class(response = json.dumps(response_data),status = 400, mimetype = 'application/json')
        
        # # File received but no filename is provided, show basic UI
        # file = request.files["file"]
        # if file.filename == "":
        #     status_code = 400
        #     # return current_app.response_class(response = json.dumps(data),status = 400, mimetype = 'application/json')
        
        # File received and it's an image, we must show it and get predictions
        if file and utils.allowed_file(file.filename):
            
            # 1. Creates unique name
            img_name = utils.get_file_hash(file)
            img_path = os.path.join(settings.UPLOAD_FOLDER,img_name)
            # 2. Stores image in '\upload'
            file.save(img_path)
            
            # 3. Sents image to be processed by the ML model
            prediction, score = model_predict(img_name)
            
            # 4. Updates Response
            response_data  = {"success": True, "prediction": prediction, "score": score}
            status_code = 200
            
            # checks for BottleNeck response
            if prediction == 'BottleNeck': 
                response_data  = {"success": False, "prediction": prediction, "score": score}
                status_code = 400
            
        # File received but it isn't an image
        else:
            flash("Allowed image types are -> png, jpg, jpeg, gif") 
            # rpse = current_app.response_class( response = json.dumps(data), status = 400, mimetype = 'application/json')    # Instead of: rpse = {"Error": 'HTTP Bad Request', "status_code": 400, "prediction": None, "score": None}
        
    return current_app.response_class( response = json.dumps(response_data), status = status_code, mimetype = settings.RPSE_MIMETYPE) 
    


@router.route("/feedback", methods=["GET", "POST"])
def feedback():
    """
    Store feedback from users about wrong predictions on a plain text file.

    Parameters
    ----------
    report : request.form
        Feedback given by the user with the following JSON format:
            {
                "filename": str,
                "prediction": str,
                "score": float
            }

        - "filename" corresponds to the image used stored in the uploads
          folder.
        - "prediction" is the model predicted class as string reported as
          incorrect.
        - "score" model confidence score for the predicted class as float.
    """
    # Get report 
    if request.method == "GET": 
        report_str = request.form.get("report")
        
    elif request.method == "POST":
        
        report_str = request.form.get("report")
        if report_str:
            report_path = settings.FEEDBACK_FILEPATH
            with open(report_path, 'a') as f:
                f.write(report_str+'\n')

    return render_template("index.html")