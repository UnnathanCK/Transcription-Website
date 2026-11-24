# Transcription-Website

## General Information

This project is a web application built using Flask that aims to make classroom learning more accessible. It provides live lecture transcription and an easy-to-use question feature to help students who may need additional support during class.

## Local Installation Instructions - Windows

You need to have Python installed on your computer.

Run the following commands in your terminal inside the project folder (this folder). These commands will create and activate a virtual environment, then install all required dependencies using `requirements.txt`.

```powershell
py -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m flask --app application init-db
```

## To Run the Flask Application Locally

Run the following command to start the Flask development server:

```powershell
python -m flask --app application run --debug
```

The application will be available at:

[http://localhost:5000](http://localhost:5000)

## Web Deployment Instructions

This project uses Gunicorn to deploy the Flask application to the web. Gunicorn only needs to be installed on the deployment server.

Install Gunicorn on the server using:

```bash
pip install gunicorn
```

To run the application using Gunicorn:

```bash
gunicorn "application:create_app()"
```

By default, Gunicorn listens on port 8000.

## Notes

- The application runs locally on port 5000 by default.
- The local web address is [http://localhost:5000](http://localhost:5000).
- If you move the project to another directory, recreate the virtual environment instead of copying the existing `venv` folder.
- Make sure the database is initialized before running the application.