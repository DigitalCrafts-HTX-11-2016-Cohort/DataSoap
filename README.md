# DataSoap
<b>Overview of Project:</b><br>
DataSoap started as a concept to build a more advanced data scrubbing system.  Datasoap allows users to be able to upload their own CSV files and have those files cleaned (scrubbed) against the national do not call list (DNC) resulting in a clean list downloadable at the users connivence.  

![alt tag](https://github.com/DigitalCrafts-HTX-11-2016-Cohort/DataSoap/blob/master/static/assets/git_screens/Screen%20Shot%202017-01-15%20at%203.54.37%20PM.png)

<b>Technologies, Frameworks and Programming Languages:</b><br>
HTML, CSS, Bootstrap, Javascript, JQuery, Python, Flask, MySql, Amazon AWS EC2

<b>Contributors:</b> <br>
Karissa Martin and Deepak Shah 

<b>Challenges faced & Solutions used:</b>
<br>1. Most of the challenges we faced involved the back end of our framework.  One of the earliest was in constructing our upload process.  We were very conscious about speed and efficiency and thus wanted to create a system where we did not have to upload and save a file directly but could have the file read and organize our data as we needed.  We implemented different approaches but ended up using a built-in library, CSV reader.  CSV reader allowed us to read files before writing and to start to parse through the data with speed and to iterate through lines that were important to us with speed and return the data using its built in next() function. 
![alt tag](https://github.com/DigitalCrafts-HTX-11-2016-Cohort/DataSoap/blob/master/static/assets/git_screens/Screen%20Shot%202017-01-15%20at%204.35.47%20PM.png)
<br><br>2.Along with speed, accuracy was paramount to DataSoap.  A challenge we faced in regards to that was being able to read a file and access information such as the headers and phone numbers and correctly populate a table in MySQL with the information normalized and intact.  Given that files could vary in the number of header columns and the column including numbers could have a variety of labels, we had to devise a solution where regardless of what was uploaded we could filter out that information accurately. The solution we implemented involved utilizing csv reader initially to parse through the data, stripping out the headers and placing them in a MySQL database and then search for numbers from what was reamaining, not relying on the header content to make that determination. From there we called a function that would normalize the data (clean it) so queries against the master list could be made and numbers on the DNC list could be accurately removed.
![alt tag](https://github.com/DigitalCrafts-HTX-11-2016-Cohort/DataSoap/blob/master/static/assets/git_screens/Screen%20Shot%202017-01-15%20at%204.36.15%20PM.png)
<br><br>3. Another challenged we faced dealt with memory and space constraints.  Our master table was fairly large but if we created and stored a new table for each upload we would quickly run out of space and it would frankly be very inefficient.  The solution we devised was to dump the data from the uploaded CSV file into a temporary table which was automatically generated upon the upload after our cleaning process.  It would only be used to make queries against the DNC master table and then delete itself upon completion. This one was tricker then it initially appeared as the path was never fixed, we allowed users to retain the file name they uploaded upon download.  We settled on using an os.path exists command as shown below.
![alt tag](https://github.com/DigitalCrafts-HTX-11-2016-Cohort/DataSoap/blob/master/static/assets/git_screens/Screen%20Shot%202017-01-15%20at%204.35.07%20PM.png)
<b>Error handling/Troubleshooting:</b></br>
Given the back end intensive nature of our project, we faced our fair share of delicate troubleshooting issues which we eventually worked out and wanted to share what we learned from each issue.
<br><br>1. Big Integer
<br><br>2. ID conflict - picking an internal id that we would not see in any file.
<br><br>3. Concatenating string and tuples, passing it in as %s or %d
<br><br>4. Error handling
