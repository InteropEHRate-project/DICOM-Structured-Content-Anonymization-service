# InteropEHRate DICOM Structured Content Anonymization Service

## Description

The DICOM Structured Content Anonymization Service has been implemented with the FastAPI web framework. The aim of the service is to anonymize the structured content of the DICOM images. This service is utilized in case that the anonymization operation cannot be performed through the S-EHR Application due to the limitation of the computational resources on the mobile phone. 

## Endpoints

The DICOM Structured Content Anonymization Service is deployed at the Healthcare Organizations involved in the InteropEHRate project and has two endpoints. 

1. **/dicom_anonymization:** The first endpoint is invoked by the user in order to upload a DICOM image at the service.
1. **/uploadfile:** Postliminary to the upload file, the uploaded DICOM image gets anonymized, and the second endpoint is invoked automatically in order for the user to download the anonymized version of the uploaded image.

## Installation Guide

1.	The service requires both [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) to be installed.
2.	Download the source code of the service from GitLab repository.
3.	Navigate to the root directory of the project **/dicom-structured-content-anonymization-service** and open a terminal.
4.	Run the command `docker-compose up -d`.
5.	The DICOM Structured Content Anonymization Service is up and running. In order to upload an image you can either visit the URL `http://[URL]:8000/dicom_anonymization` or use the cURL command  `curl -X POST -F 'dicom=@[ full path of the image]' -v http://[URL]:8000/uploadfile -J -O`.
6.	The response of the POST request is the anonymized DICOM image which was previously uploaded to the service. 

