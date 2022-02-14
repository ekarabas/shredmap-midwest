# ShredMap Midwest
CS50w Final Project

## Distinctiveness and Complexity
#### What makes this different than the projects we worked on in class?
* Interactive map with clickable markers 
* Review system using sliders
* Any review field able to be updated/added/removed at any point
* Users able to delete their own reviews
* Every field on the review is optional as long as at least one is filled in
* Total ratings system that averages all reviews for each location
* Map markers change colors based on which locations have been visited by the user
* Forms are Bootstrap Modals, multiple forms on the same page
* Utilizes Leaflet JavaScript library: https://leafletjs.com/

## Files
#### /templates/shredmap_midwest/layout.html
This file provides HTML that is consistent across all pages of the application, most notably the navbar and footer. The navbar has buttons for the user to log in, register, or log out. If the user is logged in, the navbar will note who is logged in. This file also links the required CSS files and JavaScript files to the project.

#### /templates/shredmap_midwest/register.html
This file is a form availble from the navbar that allows the user to register for an account on the website. The user will need to provide a unique username, email address, and password to create an account. Upon creating an account, the user will automatically be logged in to that account. It is structurally very similar to the registration page in previous CS50w projects.

#### /templates/shredmap_midwest/login.html
This file is a form available from the navbar that allows the user to log in to the website assuming they've already created an account. It will deny invalid logins and display appropriate error messages if the user fails to login (invalid username, password, etc). It is structurally very similar to the login page in previous CS50w projects. 

#### /templates/shredmap_midwest/index.html
This is the first page the user will see upon logging in. It displays an interactive map pinpointing each of the 100 official ski/snowboard location in the Midwest. (If ski resorts need to be added or removed, that is possible via the Django admin interface). The markers start out grey and will change to green for each resort that the user reviews. If the user deletes a review, that resort's marker will change back to grey. Clicking on any marker reveals a popup with the name of the resort as well as the city and state. Clicking on the name brings the user to a page with information on that resort.

#### /templates/shredmap_midwest/resort.html
This file will display data for the resort in question, noted by the resort ID at the end of the URL. The page will display the resort name, city, state, and website, as well as all of the current reviews for the resort. It will also aggregate all four categories (terrain park, groomers, chairlifts, overall vibe) and show the average score for each category. If the user is signed in, there will be a button to leave a review, which will reveal a modal when clicked. If the user has already left a review, there will instead be buttons to update or delete the review. The user will recieve success/error messages at the top of the page depenhding on if the review was posted/updated/deleted successfully or not. All review fields are optional as long as at least one is filled in. When the opage displays the user reviews, it only displays the fields that the user filled in, as well as the timestamp of the review, and whether it has been updated or not.

#### /static/shredmap_midwest/app.js
This file provides all the JavaScript logic for the project (aside from the built-in Bootstrap and Leaflet JS, of course). It is linked via the layout.html file. Notably, this file displays the interactive map on the homepage, as well as all of the markers. It handles the logic for changing the color of the marker based on which resorts the user has visited. It also allows the user to toggle review fields on or off when filling out a review. Review fields that are toggled off will not be included once the user submits the review, although fields can be added/removed later if the user chooses to update the review. 

#### /static/shredmap_midwest/styles.css
This file includes most of the styling for the HTML, in addition to the styling that comes along with Bootstrap. It primarily includes minor edits to ensure each element has the proper, visually-appealing amount of spacing between itself and the other elements, as well as other small style adjustments for aesthetic reasons. It also changes style for buttons and progress bars based on whether the user is viewing on a horizontal or vertical screen. If the screen becomes sufficiently vertical, the progress bars will take up the whole screen and the buttons will stack vertically rather than floating left. 

#### /static/shredmap_midwest/favicon.ico
This is a tiny 16x16 image that is displayed on the tab that this page is open on. I added it to avoid an error that kept appearing which mentioned that favicon.ico could not be found. 

#### /urls.py
This file includes paths for all the different URLs available in the project. For instance, the home page, the resort view, the login page, the register page, etc. It also includes API routes which the JavaScript file uses to retrieve data from the database. Notably, a path to retrieve information on a single resort, a path to retrieve information on all resorts, and a path to get all the resorts that the user has visited so far. 

#### /views.py
This file handles the Python logic regarding what the user sees on the screen at any given point. It validates logins and registrations, as well as retrieves the information from the database when a JavaScript fetch statement is called. Most of the logic is in the resort view. This file detects if the user posted information, such as a new review, and update to an existing review, or a delete review. Depending on what the user did on the page, this file will update the database accordingly and show the new information on the page for the user. Every time a new resort page is loaded, this file is responsible for getting the relevant information from the database to display to the user. 

#### /db.sqlite3
This is the database file that contains information on each user account, each review, and each ski resort. The database is updated via views.py when a user creates, modifies, or deletes a review, and is updated via the Django admin interface when an admin adds, removes, or modifies information on a ski resort. 

#### Other files
Other files in the project are automatically generated by Django. Some may include minor tweaks and adjustments made by me in order to maintain the functionality of the program, but for the most part, the code was generated automatically upon setting up the project. 
