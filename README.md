# Secure File Uploader & Sharer

## Overview

This project is a web application built with Django that allows users to securely upload, manage, and share files. It features user authentication and OTP (One-Time Password) verification for enhanced security during file sharing. The application is containerized using Docker for ease of setup and deployment. Its main goal is to have a personal Google Drive like application at your home under your control. 



## Key Features

* **User Authentication:** Secure user registration and login system (Leverages Django's built-in authentication).
* **File Upload:** Intuitive interface for uploading various file types.
* **File Management:** Users can view and manage their uploaded files.
* **Secure File Sharing:**
    * Share files with specific users.
    * **OTP Verification:** Option to require recipients to enter a One-Time Password before accessing shared files, adding an extra layer of security.
* **"Shared With You" View:** Users can easily see files that have been shared with them.
* **Containerized Deployment:** Uses Docker and Docker Compose for consistent development and deployment environments.


## Technologies Used

* **Backend:** Python, Django
* **Database:** *(**Note to User:** Specify the database used, e.g., PostgreSQL, SQLite, MySQL - Check your `settings.py`)*
* **Frontend:** HTML, CSS, JavaScript *(**Note to User:** Mention any specific frameworks/libraries used, e.g., Bootstrap, jQuery, etc.)*
* **Containerization:** Docker, Docker Compose
