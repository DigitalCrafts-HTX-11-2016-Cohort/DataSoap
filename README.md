# DataSoap

Link to live site: <a href='http://35.166.251.127'>DataSoap</a><br>
<br><b>Overview of Project:</b><br>
DataSoap started as a concept to build a more advanced data scrubbing system.  Datasoap allows users to be able to upload their own CSV files and have those files cleaned (scrubbed) against the national do not call list (DNC) resulting in a clean list downloadable at the users connivence.  

![alt tag](https://github.com/DigitalCrafts-HTX-11-2016-Cohort/DataSoap/blob/master/static/assets/git_screens/Screen%20Shot%202017-01-15%20at%203.54.37%20PM.png)

<b>Technologies, Frameworks and Programming Languages:</b><br>
HTML, CSS, Bootstrap, Javascript, JQuery, Python, Flask, MySql, Amazon AWS EC2

<b>Contributors:</b> <br>
Karissa Martin and Deepak Shah 

<b>Challenges faced & Solutions used:</b>
<br>1. Most of the challenges we faced involved the back end of our framework.  One of the earliest was in constructing our upload process.  We were very conscious about speed and efficiency and thus wanted to create a system where we did not have to upload and save a file directly but could have the file read and organize our data as we needed.  We implemented different approaches but ended up using a built-in library, CSV reader.  CSV reader allowed us to read files before writing and to start to parse through the data with speed and to iterate through lines that were important to us efficiently and return the data using its built in next() function. 
![alt tag](https://github.com/DigitalCrafts-HTX-11-2016-Cohort/DataSoap/blob/master/static/assets/git_screens/Screen%20Shot%202017-01-15%20at%204.35.47%20PM.png)
<br><br>2.Along with speed, accuracy was paramount to DataSoap.  A challenge we faced in regards to that was being able to read a file and access information such as the headers and phone numbers and correctly populate a table in MySQL with the information normalized and intact.  Given that files could vary in the number of header columns and the column including numbers could have a variety of labels, we had to devise a solution where regardless of what was uploaded we could filter out that information accurately. The solution we implemented involved utilizing csv reader initially to parse through the data, stripping out the headers and placing them in a MySQL database and then search for numbers from what was reamaining, not relying on the header content to make that determination. From there we called a function that would normalize the data (clean it) so queries against the master list could be made and numbers on the DNC list could be accurately removed.
![alt tag](https://github.com/DigitalCrafts-HTX-11-2016-Cohort/DataSoap/blob/master/static/assets/git_screens/Screen%20Shot%202017-01-15%20at%204.36.15%20PM.png)
<br><br>3. Another challenged we faced dealt with memory and space constraints.  Our master table was fairly large but if we created and stored a new table for each upload we would quickly run out of space and it would frankly be very inefficient.  The solution we devised was to dump the data from the uploaded CSV file into a temporary table which was automatically generated upon the upload after our cleaning process.  It would only be used to make queries against the DNC master table and then delete itself upon completion. This one was tricker then it initially appeared as the path was never fixed, we allowed users to retain the file name they uploaded upon download.  We settled on using an os.path exists command as shown below.
![alt tag](https://github.com/DigitalCrafts-HTX-11-2016-Cohort/DataSoap/blob/master/static/assets/git_screens/Screen%20Shot%202017-01-15%20at%204.35.07%20PM.png)
<br><br><b>Error handling/Troubleshooting:</b></br>
Given the back end intensive nature of our project, we faced our fair share of delicate troubleshooting issues which we eventually worked out and wanted to share what we learned from each issue.
<br><br>1. Big Integer - Given that we took striped the phone numbers to make them 10 digit integers we naturally gave them a setting of int in MySQL.  As we loaded the master DNC data set, we quickly realized that the enitre data set wasn't loading.  For some reason the entire list of numbers stopped at 2147483647.  We were perplexed because the code we wrote looked spot on.  With the help of our instructor and stack overflow, we realized that in MySQL integers have a maximum value and that in our case we need to use big int to represent any number above 2147483647.<br>
![alt tag](https://github.com/DigitalCrafts-HTX-11-2016-Cohort/DataSoap/blob/master/static/assets/git_screens/Screen%20Shot%202017-01-15%20at%204.48.59%20PM.png)
<br><br>2. ID conflict - picking an internal id that we would not see in any file.  We've had the habit of labeling our internal id tag in MySQL as id for simplicity sake.  Yet realized that in taking in any headers from user files we may run into the issue of duplication as others may have an id header.  To resolve this we labeled our internal header DNCInternalID to avoid any errors.<br>
![alt tag](https://github.com/DigitalCrafts-HTX-11-2016-Cohort/DataSoap/blob/master/static/assets/git_screens/Screen%20Shot%202017-01-15%20at%204.49.14%20PM.png)
<br><br>3. Concatenating string and tuples, passing it in as %s or %d.  File path after file path we found ourselves concatenating to direct files in and out.  When we started we kept running into erros involving concatenating strings and tuples but resolved it by passing in the data as %s or %d.
![alt tag](https://github.com/DigitalCrafts-HTX-11-2016-Cohort/DataSoap/blob/master/static/assets/git_screens/Screen%20Shot%202017-01-15%20at%208.19.20%20PM.png)
<br><br>4. Error handling.  In general, like any project you spend a fair bit of time with general error handling.  Because of all the different routes and databases, we knew we could run into issues if we didn't stay organized.  To this end, we organized the data in classes (users and filename) and were cognizant of how we wanted to route between our static pages and dynamic content.  We started the project by building a roadmap and although we made adjustments along the way, modeling our design this way made implementing those changes more agile.
<br>
<br><b>MVP and Stretch Goals:</b>
<b>MVP</b><br>
1.  Build a data scrubbing system where users can upload files and we can compare it against the national do not call list and output a downloadable file with only numbers that are not on the list.<br>
2.  Allow users to register for this service with a log in username and for us to be able to keep track of who accesses this service.<br>
3.  UI layout that is easy to use and intuitive.  All the research we've done on sites similar to this look quite outdated and we wanted users to have a pleasant and easy to use experience with our upload and download features.<br>
4.  Basic dashboard where users can access history and data about their previous usage and a place where downloads could be archived for convienience.
<br><br><b>Stetch Goals</b><br>
1.  Adding a quick search feature so an individual can quickly search for one number without having to upload a file.<br>
![alt tag](https://github.com/DigitalCrafts-HTX-11-2016-Cohort/DataSoap/blob/master/static/assets/git_screens/census_logo.jpg)
<br>2.  Adding census bureau api data so we can give additional information about individuals on call lists to better aid user.
<br>3.  Adding stripe api to allow payments for professional serivce.
![alt tag](https://github.com/DigitalCrafts-HTX-11-2016-Cohort/DataSoap/blob/master/static/assets/git_screens/Stripe_logo%2C_revised_2016.png)
<br>4.  Geocoding - adding latitude and longitude data to better aid users by giving them geographic location.
<br>
<b><br>Contribution we'd like to be added:</b><br>
1.  Census data - We ended up running out of time to implement this feature but we certainly want it to be added in the future.  It is something we shall revisit soon.<br>
2.  Geocoding - Also ended up running out of time for implementation and is high on the wish list to be added in the future.
