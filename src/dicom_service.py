import shutil
import os
import datetime
import uvicorn
import pydicom

from fastapi import FastAPI, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from pydicom.filereader import InvalidDicomError
from pydicom import dcmread
from pydicom.data import get_testdata_file
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/uploadfile")
async def upload_file(dicom: UploadFile = File(...)):
	filepath, filename, dicom_file, input_name, output_name = initialize_variables(dicom)
	input_full_path = filepath + input_name
	with open(input_full_path, "wb") as buffer:
		shutil.copyfileobj(dicom_file, buffer)
	is_dicom = is_dicom_file(input_name)
	if is_dicom == True:
		anonymized_dicom = anonymize_dicom(filepath, output_name, input_full_path)
		delete_dicom(input_full_path)
		print("File ", filename, " was successfully anonymized.")
		def iterfile():
			with open(anonymized_dicom, mode="rb") as file_like:
				yield from file_like
			delete_dicom(anonymized_dicom)
		response = StreamingResponse(iterfile(), media_type="application/dicom")
		response.headers["Content-Disposition"] = "attachment; filename=" + anonymized_dicom.rsplit('/',1)[1]
		return response
	else:
		message = "Anonymization process was not applied to this file. File \'" + filename + "\' is NOT in DICOM format."
		json = {"message": message}
		return JSONResponse(status_code=400, content=json)


@app.get("/dicom_anonymization", response_class=HTMLResponse)
async def load_webpage():
	return """
	<!DOCTYPE html>
	<html>
		<body>
			<form action="/uploadfile" method="post" enctype="multipart/form-data">
				<div> Select image to upload: </div>
				<input type="file" id="dicom" name="dicom">
				<input type="submit" value="Upload Image" name="submit">
			</form>
		</body>
	</html>
	"""

def is_dicom_file(filename):
	try:
		filepath = get_testdata_file(filename)
		ds = dcmread(filepath)
		return True
	except pydicom.filereader.InvalidDicomError:
		return False

def initialize_variables(dicom):
	current_datetime = datetime.datetime.now()
	date_time = current_datetime.strftime("%Y-%m-%d_%H.%M.%S")

	filepath = "/venv/lib/python3.8/site-packages/pydicom/data/test_files/dicomdirtests/"

	filename = dicom.filename
	dicom_file = dicom.file

	input_name = os.path.splitext(filename)[0]
	fileExtension = os.path.splitext(filename)[1]
	input_name = input_name + "_" + date_time + fileExtension
	output_name = "anonymized_" + input_name

	return filepath, filename, dicom_file, input_name, output_name

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
