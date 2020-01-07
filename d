@app.route('/uploadFile',methods=['POST'])
def uploadFile():
    responseData=""
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            responseData="No file part"
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            responseData="No selected file"
        if file: 
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                responseData="File uploaded successfully"
            else:
                responseData="In valid Extension"
        else:
            responseData="Error in uploading file"
    r = make_response(responseData)
    r.mimetype = 'text/plain'
    return r