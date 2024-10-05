# YorkEats
A website designed to help students, visitors and more find open locations to eat at York University. Created by Sean Murphy.

## Screenshots

![image](https://github.com/user-attachments/assets/88ff3537-49f8-4395-b4f9-5b499343d8f5)
![image](https://github.com/user-attachments/assets/0f18a34a-c2fb-437e-9c7e-ffb8ed1930ce)

[![Youtube Demonstration Video](http://img.youtube.com/vi/jAnrKluaLBQ/0.jpg)](https://youtu.be/jAnrKluaLBQ)  
Click above to view a video demo of the website! 

## Summary
### Purpose
Help my university's community by providing a quick and easy way to find, locate and filter through open restaurants and eateries on campus. 

### Features
A number of features required external research as referenced in the code. Some of these features are listed below
* Restaurant Filters using JavaScript
* Google API requests
* Web scraping with Beautiful Soup
* Various Boostrap Components (collapse, dropdown, etc)

## User Guide
### Find places to eat at York
1. Navigate to All Locations using the navbar
2. Select filters and search if needed

### Find currently open restaurants
1. Navigate to "What's Open Now?" using the navbar
2. Select filters and search if needed

### Find out whats open at a selected time
1. Navigate to "What's Open Later?" using the navbar
2. Select a time
3. Select filters and search if needed

### Rate a location
1. Login or create an account by clicking the navbar's login button
3. Rate the desired post using the five stars

## Admin Actions
### Edit a location's photo
1. Login to a super user account
2. Click edit on the targeted post
3. Upload an image and submit

## Setup Guide
1. Run makemigrations and migrate
2. Run the scrape_dir command (Updates JSON data)
3. Run the update_db command (Updates models)
4. Run the places_request command (Uploads google maps addresses and images to the website, requires an API key)

## File Descriptions
### dining_dir.json
Contains the data in JSON format from both the Google Places API and the scraped York Dining Directory

### places_request.py
Django manage.py command that performs an API request for the addresses and images of locations provided in the dining_dir.json JSON data.

### scrape_dir.py
Scrapes the York University dining directory for data on places to eat at York (https://www.yorku.ca/foodservices/dining-directory/). Uploads the data to dining_dir.json

### update_db.py
Updates django models with the dining_dir.json data

### home_styles.css
Styling for the What's Open Now, What's Open Later and All Locations pages

### login_styles.css
Styling for the login and register page

### home.js
Javascript for the What's Open Now, What's Open Later and All Locations pages. Controls the following features
* Admin image edit button and form
* User rating submissions
* Filter behavior
* Animations

### all.html
HTML for all locations page

### index.html
HTML for What's Open Now page

### later.html
HTML for What's Open Later page

### layout.html
Navbar

### Login.html and Register.html
Login and register pages

### later.js
Javascript specifically for the What's Open Later page

### models.py
Contains the models for both Places (places to eat) and user ratings.

### views.py
See comments in file for an explanation of each view.

### media/images directory
Stores the images for each Place model.
