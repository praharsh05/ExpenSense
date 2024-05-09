# ExpenSense

ExpenSense is an automated expense management web application for Small and Medium-Scale Enterprises

## Installation

Use Anaconda to create a virtual environment and install the dependencies from environment.yml file.

```bash
conda env create -f environment.yml
```

## Activating Conda Environment

```bash
conda activate expensense
```

## Make Database Migrations

Navigate to the directory containing the file `manage.py` and then make database migrations by running the following commands

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

## Run the Django Web Server

To run the Django web server, navigate to the directory containing `manage.py` file and execute the following command

```bash
python manage.py runserver
```

## Codebase

the codebase is divided into multiple directories to implement the Don't Repeat Yourself (DRY) design principle. the major component included are:

```
expensense_main
|
|-expensense
|   |
|   |-migrations
|   |-templatetags
|
|-expensense_main
|
|-media
|   |
|   |-receipts
|   |-signatures
|
|-static
|   |
|   |-css
|   |-images
|   |-js
|
|-templates
|
|-manage.py
```

### expensense directory

The expensense directory contains the main app and all its logic divided into multiple files.
The `admin.py` is use to register the models for the superuser or site admin to view and make modifications, if and when necessary.
The `apps.py` is use to specify app wide functionality such as creation of default `categories` and to register the use of `signals.py` file.
The forms utilised in the app are defined in `forms.py`.
The database models or database schema is defined in `models.py`.
The functionality related to external OCR API in `ocr_api.py`. 
Functionality related to report generation can be found in `report.py`. 
Logic related to the auto approval engine in `signals.py`. 
The logic related to signature extraction and matching in `signature_matching.py`. 
The routing and definition of urls are in `urls.py`. 
The business logic or the core app functionality is in `views.py`. 
Finally, unit tests are written in `tests.py`.

### expensense_main directory

This directory contains the essential project files such as `settings.py` which contains all the settings for the Django project, `urls.py` which is the original router of the django project and routes the requests for the expensense app to the `urls.py` in the `expensense` directory, and `wsgi.py` file which can be utilised when the web application is deployed.

### media directory

this directory will be updated everytime a user submits a file to be stored on the server. In this project, the media directory will have 3 directories mainly, `receipts` containing the receipt images submitted by the user when submitting expense form, `signatures` containing the signature images submitted by the user at the time of registration, and `signature_test` containg signatues used in testing.

### static directory

this directory contains all the static files, it is also divided into 3 sub directories, `css` containing the custom css file, `images` containing the images and logos used throughout the web application, and `js` containing the different JavaScript files.

### templates directory

this directory contains the HTML template files utilised by the Django Template engine in order to render content to client browsers.

## Core Functionalities

the core functionalities are defined in the `views.py` file. this file has class-based views achienved by inherting from `django.views.View` class. the different views are as follows:

### 1. IndexView

this class is responsible for the home page of the web application.

![homepage](https://github.com/praharsh05/ExpenSense/assets/75966397/2e847962-545e-4592-9ff6-eb2c19b48c79)


### 2. RegisterStep1View

this class defines the step 1 of the registration process utilising sessions to store user data until step 2 is completed

### 3. RegistrationStep2View

this class defines the serving of user's role specific step 2 form and handling the submission of these forms in order to create company, team and user instances in the database.

### 4. LoginView

this class handles securly loging in a registered user.

### 5. LogoutView

this class handles securly loging out a user.

### 6. DashboardView

this class contains the functionality of creating a user's role and permission specific dashboard. this class has different methods, each corresponding to different functional components on the dashboard. these are `expense_graph_view` for retriving the data for the expense graph, `overall_summary` for total expenditure and category-wise summary of the expenses, `pending_requests` for displaying those requests that have a pending status for manager and manager approved status for admin, `approved_requests` for displaying the approved requests by the managerial users and the final approved request for employees, `get_last_three_reports` for generating pdf reports for last three calendar months, and the `get` method to combine all the aforementioned methods.

![expensense_dashboard](https://github.com/praharsh05/ExpenSense/assets/75966397/41861058-2af3-448f-ab3d-28b14dcf89b7)


### 7. LogExpenseView

this class handles the `get` and `post` requests of expense form. when a post request is made `calculate_similarity` method is run on the submitted receipt image and user's signature which checks for the signature similarity. the `calculate_similarity` is defined in the `signature_matching.py` file. once signature matching is done, the method creates an expense instance in the expense model.

![log_expense](https://github.com/praharsh05/ExpenSense/assets/75966397/e8bce0bc-fa7d-4a96-8fe2-6212dd930d01)


### 8. OcrApiView

this class is creates the OCR API which is utilised to autofill the expense form by reading the text from receipt image submitted by user. this class has only `post` method which is used to create a temp file to pass to the `results` method which is defined in `ocr_api.py`. The `results` method submits the file to the external api to read data from the image and then tries to find the amount and date from the receipt image and returs a JSON response to the front end.

### 9. AllExpenseView

this class aggregates the expenses based on role of the user, orders them in the decreasing order of the expense date and then paginates these expenses by 10 expenses per page.

![expensense_all_expenses](https://github.com/praharsh05/ExpenSense/assets/75966397/28898bb8-6cd6-42e8-8d85-93c866479b19)


### 10. ApprovalConditionView

this class is used to get the existing approval conditions by querying the `ApprovalConditions` model for users with roles other than employees.

![approval_conditions](https://github.com/praharsh05/ExpenSense/assets/75966397/e35f3aa7-7f59-4c1e-abd0-5ccefa3384b9)


### 11. SetApprovalConditions

this class is used to handle setting the approval conditions for different managerial users.

### 12. PendingRequestView

this class is used to show the paginated expense instances which have a staus `pending` for managers and employees, and `manager approved` for admins in their respecive teams and companies.

![pending_requests](https://github.com/praharsh05/ExpenSense/assets/75966397/c58d6f1a-a472-4f2a-8520-f26b5bad6821)


### 13. ExpenseView

this class is utilised to get the expense detail of a particular expense. the `get` method takes in the `request` and `expense_id` as arguments to query the expense model.

![expense_detail](https://github.com/praharsh05/ExpenSense/assets/75966397/c858343b-b2b2-439b-823b-e2aeaea19af4)


### 14. ApproveExpenseView

this class is used to update an expense instance when a managerial user approves the request, updating the status, timestamp and boolean fields for manager and admin (dependent on approver's role).

### 15. DenyExpenseView

this class adds the functionality of denying an expense request by managers or admins.

### 16. GenerateExpensePDFView

this class handles the requests for generating the PDF report of the expenses based on user role and start and end date. these dates are passed to the `generate_pdf` method defined in `reports.py`.

![generate_pdf](https://github.com/praharsh05/ExpenSense/assets/75966397/b2e0fe45-f793-4c31-990f-424c23da668c)


### 17. BudgetView

this class is used to display the budget set by managerial users, for admin they are shown the company budget and for managers they are shown their team budget by querying the company and team model, respectively.

### 18. teams method

this method acts as an API and is used to used to query the `Team` model to get the teams in a company. this method is utilised at the time of registration of employees. when a user with role of employee selects a company on step-2 of the registration form, the JavaScript method in `my_script.js` makes a `FETCH` requests to this method which in turn queries the `Team` model and then returns a JSON response. this response is then unpacked and the received teams are populated for selection by the user.

## Keys and Contact

in order to safeguard the application from potential threats, the Django SECRET_KEY and OCR.Space API key has been kept private. if you wish to run the application on you local server please contact on `2738037d@student.gla.ac.uk` for the keys.
