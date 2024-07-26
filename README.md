![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **May 14, 2024**

## Reminders

- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

Happy coding!

This is my third project within the fullstack development at Code Institute. This project is about analyzing syúrvey data using Python. 
The aim of the project is to build an application that analyzes survey data and provide actionable insights from an inputted dataset.
This application is a command-line interface (CLI) design for easy data import and analysis 

Features:
The potential features of the project includes the following:
1.Data import
- Allows users to import survey results via the terminal or by upploading a file from the computer. In additio the data import function supports multiple file fromat (CSV, Excel) 
2. Data parse and analysis
- Parse the imported data and validate data for consistency and completeness. Calculate basic statistics (mean) and identify trends and patterns (e.g using histogram )
- 
3.Visualization
- Generate visual representations of the data (graphs) by using liberaries like Matplotlib, Seaborn or plotly for interactive plots.



