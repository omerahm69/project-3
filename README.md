![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

This is my third project within the Fullstack development at Code Institute. This project is about analyzing survey data using Python. 

The aim of the project is to build an application that analyzes survey data and provides actionable insights from an inputted dataset.

This application is a command-line interface (CLI) design, for easy data import and analysis. 

Features:

The potential features of the project include the following:

1. Data import

- Allows users to import survey results via the terminal or by uploading a file from the computer. The data import function supports multiple file formats (CSV, Excel). 

2. Data parse and analysis

- Parse the imported data and validate the data for consistency and completeness. Calculate basic statistics (mean/average) and identify trends and patterns (e.g. using histogram )

3. Visualization

- Generate visual representations of the data (graphs) by using libraries like Matplotlib, Seaborn or Plotly for interactive plots.
  
![Figure_1 age](https://github.com/user-attachments/assets/0cf6bc35-88c5-4612-8abe-62499c30ca97)

  ![Figure_2-schooldegree](https://github.com/user-attachments/assets/b2b6d6e6-ca3e-41dd-ae6f-4225a1ac571d)
  
![Figure_3 gender distribution](https://github.com/user-attachments/assets/fa98de2c-b509-497d-903c-e3082243a1b6)

4.Data exportation for the user in csv format
  - Allow users to export the analysis into various forms like Excel and CSV.

The application program includes four functions and follows as below:


![Application](https://github.com/user-attachments/assets/d81dbccf-dfb8-4910-ba99-39f3cb7108b9)

The survey data is from Kaggle, 2016 New Coder "2016-FCC-New-Coders-Survey-Data.csv"
But due to the limitations 

Testing: Validator testing

![Skärmbild 2024-07-27 113528 Styling checker ](https://github.com/user-attachments/assets/ce814ff4-29fb-4607-92b6-de0e2a6842f6)

Unfixed Bugs 
-It is the use of Pandas library to change the survey data into a data frame before doing analysis. When I deployed to the Heruku I realized that pandas packages are not included in the dependancies and I couldn't navigate through the application after deployment. 
- Since it is always common that survey data includes different types of data, like numerical and categorical and also some missing data. The idea was to deal with those kinds of data, seperate them and prepare the data seperately doing analysis, but I didn't manage to do that in this application. This will be fixed in the future. 

Deployment

Heruku is a platfrom designed to host dynamic websites and it's built to handle back end languages and that is why we are using Heruk. 
- To deploy to the platform one needs to have an account by signing up to the Heruku website.
Deployment to Heruku is different from deployment to Github pages since there are many steps.
- In order for the project to run on Heruku, we need to install dependancies. This list of dependencies will go in our requirement.txt file and to create the list of requirements we use the following command in the terminal '' pip3 freeze > requirements.txt. Heruku searches for this exact file name as is it builds the project and installs the requirements into the application.
- After having a Heruku account and singning in the website, we will get into the Heruku dashboard and there we can create our first app. App is short for web application. " Create new "app" button and giv it a name and select your location region "Europe"
- From the tabs up, go to the setting and choose " Config Vars" which is also known as enviroment variables where we can store secret data. In the field for key, enter CREDS, all capital letters. And then copy the entire creds.json and paste it into the value field, click "Add"
- The Next step is to add a couple of buildpacks, "python and node.js" to our application. Click "Add buildpack" and " save changes"
- We then go to the deployment section and choose the deployment method → select Github and then confirm that we want to connect to Github. Now we can search for our repository name and then click " Search" and then we click connect to link up our Heruku app to our Github repository.
- We can then scroll down and choose one of two options: Automatic deploy or manually deploy.
- Now the app is built, and we can see the logs as it runs, it installs Pyhthon and each of the dependencies we have listed in our requirements.txt. Finally we see the "App was successfully deployed" message and a button to our deployed link.


If you have forked or cloned the repository the steps to deploy are:
1. On GitHub.com, navigate to your repository
2. Navigate to the settings tab
3. Click on the tab called 'pages' on the left hand side
4. From the source drop down list under the heading Build and deployment, select main.
5. The page will then provide the link to the website https://omerahm69.github.io/project-3/

Credit

Content

. Process from the Code Institute Love Sadwishes project was used to help create this website- CI . Python code help was taken from w3schhols-W3Schools








