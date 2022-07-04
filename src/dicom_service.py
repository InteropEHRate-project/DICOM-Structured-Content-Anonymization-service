import base64
import datetime
import os
import pydantic
import pydicom
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from io import BytesIO
from pydicom import dcmread, dcmwrite
from pydicom.data import get_testdata_file
from pydicom.filebase import DicomBytesIO
from pydicom.filereader import InvalidDicomError

app = FastAPI()

@app.post("/uploadfile")
async def upload_file(request: Request):
    data: bytes = await request.body()
    filepath, input_name, output_name = initialize_variables()
    input_full_path = filepath + input_name  
    dicom = dcmread(BytesIO(data))
    dcmwrite(input_full_path, dicom)         
    is_dicom = is_dicom_file(input_name)
    if is_dicom == True:
        anonymized_dicom = anonymize_dicom(filepath, output_name, input_full_path)
        delete_dicom(input_full_path)
        message = "DICOM was successfully anonymized!"
        with open(anonymized_dicom, "rb") as file_like:
            encoded_string = base64.b64encode(file_like.read())
            data = encoded_string.decode()
        delete_dicom(anonymized_dicom)
        json = {"status": "200", "message": message, "data": data}
        return JSONResponse(status_code=200, content=json)
    else:
        message = "Anonymization process was not applied to this file since it is NOT in DICOM format."
        json = {"status": "400", "message": message}
        return JSONResponse(status_code=400, content=json)

def is_dicom_file(filename):
	try:
		filepath = get_testdata_file(filename)
		ds = dcmread(filepath)
		return True
	except pydicom.filereader.InvalidDicomError:
		return False

def initialize_variables():
	current_datetime = datetime.datetime.now()
	date_time = current_datetime.strftime("%Y-%m-%d_%H.%M.%S")

	filepath = "/venv/lib/python3.8/site-packages/pydicom/data/test_files/dicomdirtests/"
	filename = "dicom"

	input_name = filename + "_" + date_time
	output_name = "anonymized_" + input_name

	return filepath, input_name, output_name

def anonymize_dicom(path, output_name, input_full_path):
	output_full_path = path + output_name
	cmd = "dicom-anonymizer " + input_full_path + " " + output_full_path
	os.system(cmd)
	return output_full_path

def delete_dicom(filepath):
	if os.path.exists(filepath):
		os.remove(filepath)

if __name__ == '__main__':
	uvicorn.run("dicom_service:app", host="0.0.0.0", port=8000)