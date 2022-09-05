# InteropEHRate DICOM Structured Content Anonymization Service

## Description

The DICOM Structured Content Anonymization Service has been implemented with the FastAPI web framework. The aim of the service is to anonymize the structured content of the DICOM images. More specifically, the service takes as input a DICOM image in its original form (in Base64 encoded format) and returns its anonymized version. This service is utilized in case that the anonymization operation cannot be performed through the S-EHR Application due to the limitation of the computational resources on the mobile phone.

## Endpoints

The DICOM Structured Content Anonymization Service is deployed at the Healthcare Organizations involved in the InteropEHRate project and has one endpoint.

1. **/uploadfile:** This endpoint is invoked by the user in order to upload a DICOM image to the service.

## Installation Guide

1.	The service requires both [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) to be installed.
2.	Download or clone the folder with the source code of the service from GitHub repository.
3.	Navigate to the root directory of the project **/dicom-structured-content-anonymization-service** and open a terminal.
4.	Run the command `docker-compose up -d`.
5.	The DICOM Structured Content Anonymization Service is up and running. In order to upload an image you can use the DICOM Structured Content Anonymization Library.
6.	The response of the POST request is the anonymized DICOM image (in Base64 encoded form) which was previously uploaded to the service. 

<ins>Response:</ins> If the anonymization operation has been successfully applied to the DICOM image, the response will be as follows and the anonymized DICOM image will be stored within the **data** key-value pair.

```
{
    "status":"200",
    "message":"DICOM was successfully anonymized!",
    "data":"$data"
}
```

<ins>Error response:</ins> If the uploaded file is not in DICOM format the response will be as follows.

```
{
    "status":"400",
    "message":"Anonymization process was not applied to this file since it is NOT in DICOM format."
}
```
