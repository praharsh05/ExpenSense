import importlib
from unittest.mock import patch
from django.test import TestCase, Client
import os
from django.conf import settings
from .views import *
from expensense.forms import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.files.uploadedfile import SimpleUploadedFile

FAILURE_HEADER = f"{os.linesep}TEST FAILURE{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"


class SetupTest(TestCase):
    """
    Setup tests for the new Expensense project, original taken from 
    https://github.com/tangowithcode/tango_with_django_2_code.git,
    The tests probe the file structure of the project.
    """

    def setUp(self):
        """ 
        Set up the base_dir and expensense_dir variable corresponding
        to the project directory and app directory
        """
        self.project_base_dir = os.getcwd()
        self.expensense_dir = os.path.join(
            self.project_base_dir, 'expensense')
        self.template_tag_dir = os.path.join(self.expensense_dir,
                                              'templatetags')
        self.templates_dir = os.path.join(self.project_base_dir, 'templates')
        self.expensense_template_dir = os.path.join(self.templates_dir,
                                                     'expensense')

    def test_project_created(self):
        """
        Tests whether the expensense_main configuration directory is present
         and correctectly defined.
        """
        directory_exists = os.path.isdir(os.path.join(
            self.project_base_dir, 'expensense_main'))
        is_python_package = os.path.isfile(
            os.path.join(self.expensense_dir, '__init__.py'))
        settings_module_exists = os.path.isfile(os.path.join(
            self.project_base_dir, 'expensense_main', 'settings.py'))
        wsgi_module_exists = os.path.isfile(os.path.join(
            self.project_base_dir, 'expensense_main', 'wsgi.py'))
        urls_module_exists = os.path.isfile(os.path.join(
            self.project_base_dir, 'expensense_main', 'urls.py'))

        self.assertTrue(directory_exists,
                        f"{FAILURE_HEADER}expensense project configuration \
                              directory doesn't exist{FAILURE_FOOTER}")
        self.assertTrue(is_python_package, f"{FAILURE_HEADER}The expensense \
                        directory is not a python package directory. Did you \
                        use the startapp command?{FAILURE_FOOTER}")
        self.assertTrue(settings_module_exists,
                         f"{FAILURE_HEADER}Your project's urls.py module does \
                              not exist.Did you use the startproject command? \
                                {FAILURE_FOOTER}")
        self.assertTrue(wsgi_module_exists,
                         f"{FAILURE_HEADER}Your project's urls.py module does \
                              not exist.Did you use the startproject command? \
                                {FAILURE_FOOTER}")
        self.assertTrue(urls_module_exists,
                         f"{FAILURE_HEADER}Your project's urls.py module does \
                              not exist.Did you use the startproject command? \
                                {FAILURE_FOOTER}")

    def test_app_created(self):
        """
        Test for the expensense app directory and whether it has the required
        files and is a python package.
        """
        directory_exists = os.path.isdir(self.expensense_dir)
        is_python_package = os.path.isfile(
            os.path.join(self.expensense_dir, '__init__.py'))
        admin_module_exists = os.path.isfile(
            os.path.join(self.expensense_dir, 'admin.py'))
        apps_module_exists = os.path.isfile(
            os.path.join(self.expensense_dir, 'apps.py'))
        forms_module_exists = os.path.isfile(
            os.path.join(self.expensense_dir, 'forms.py'))
        model_module_exists = os.path.isfile(
            os.path.join(self.expensense_dir, 'models.py'))
        ocr_api_module_exists = os.path.isfile(
            os.path.join(self.expensense_dir, 'ocr_api.py'))
        report_module_exists = os.path.isfile(
            os.path.join(self.expensense_dir, 'report.py'))
        signals_module_exists = os.path.isfile(
            os.path.join(self.expensense_dir, 'signals.py'))
        views_module_exists = os.path.isfile(
            os.path.join(self.expensense_dir, 'views.py'))
        url_module_exists = os.path.isfile(
            os.path.join(self.expensense_dir, 'urls.py'))
        

        self.assertTrue(
            directory_exists, f"{FAILURE_HEADER}The expensense app directory \
                  does not exist. {FAILURE_FOOTER}")
        self.assertTrue(
            is_python_package, f"{FAILURE_HEADER}The expensense directory is \
                  not a python package directory.{FAILURE_FOOTER}")
        self.assertTrue(
            admin_module_exists, f"{FAILURE_HEADER}The expensense directory \
                  is missing admin.py file.{FAILURE_FOOTER}")
        self.assertTrue(
            apps_module_exists, f"{FAILURE_HEADER}The expensense directory \
                  is missing apps.py file.{FAILURE_FOOTER}")
        self.assertTrue(
            forms_module_exists, f"{FAILURE_HEADER}The expensense directory \
                  is missing forms.py file.{FAILURE_FOOTER}")
        self.assertTrue(
            model_module_exists, f"{FAILURE_HEADER}The expensense directory \
                  is missing models.py file.{FAILURE_FOOTER}")
        self.assertTrue(
            ocr_api_module_exists, f"{FAILURE_HEADER}The expensense directory \
                  is missing ocr_api.py file.{FAILURE_FOOTER}")
        self.assertTrue(
            report_module_exists, f"{FAILURE_HEADER}The expensense directory \
                  is missing report.py file.{FAILURE_FOOTER}")
        self.assertTrue(
            signals_module_exists, f"{FAILURE_HEADER}The expensense directory \
                  is missing signals.py file.{FAILURE_FOOTER}")
        self.assertTrue(
            views_module_exists, f"{FAILURE_HEADER}The expensense directory \
                  is missing views.py file.{FAILURE_FOOTER}")
        self.assertTrue(
            url_module_exists, f"{FAILURE_HEADER}The expensense directory \
                is missing urls.py file.{FAILURE_FOOTER}")


    def test_expensense_app_configured(self):
        """
        Test to confirm if expensense app was added to the INSTALLED_APPS list.
        """
        app_configured = 'expensense' in settings.INSTALLED_APPS

        self.assertTrue(
            app_configured, f"{FAILURE_HEADER}The expensense app is \
                missing from the setting's INSTALLED_APPS list.\
                    {FAILURE_FOOTER}")
    
    def test_template_tags_directory_created(self):
        """
        Test to confirm if the templatetags directory is created inside
        expensense app directory and contains the required files
        """
        directory_exists = os.path.isdir(os.path.join(
            self.expensense_dir, 'templatetags'))
        is_python_package = os.path.isfile(
            os.path.join(self.template_tag_dir, '__init__.py'))
        custom_filters_module_exists = os.path.isfile(os.path.join(
            self.template_tag_dir, 'custom_filters.py'))
        
        self.assertTrue(
            directory_exists, f"{FAILURE_HEADER}The templatetags directory \
                  does not exist. {FAILURE_FOOTER}")
        self.assertTrue(
            is_python_package, f"{FAILURE_HEADER}The templatetags directory is \
                  not a python package directory.{FAILURE_FOOTER}")
        self.assertTrue(
            custom_filters_module_exists, f"{FAILURE_HEADER}The templatetags \
                directory is missing custom_filters.py file.{FAILURE_FOOTER}")
    
    def test_template_directory_created(self):
        """
        Test to confirm if the template directory was created
        """

        directory_exists = os.path.isdir(os.path.join(
            self.project_base_dir, 'templates'))
        expensense_directory_exists = os.path.isdir(os.path.join(
            self.templates_dir, 'expensense'))
        
        self.assertTrue(
            directory_exists, f"{FAILURE_HEADER}The templates directory does \
                not exist. {FAILURE_FOOTER}")
        self.assertTrue(
            expensense_directory_exists, f"{FAILURE_HEADER}The expensense \
                template directory does not exist. {FAILURE_FOOTER}")


class IndexTests(TestCase):
    """
    Class for index page tests
    """
    
    def test_index_view_exists(self):
        """
        Test if the IndexView exists as a class
        """
        self.assertTrue(hasattr(IndexView, '__class__'), f"{FAILURE_HEADER} \
                        The IndexView does not exist.{FAILURE_FOOTER}")
    
    def test_index_view_rendering_using_url(self):
        """
        Test to check if the index page is being rendered with the correct
        status code
        """

        client = Client()

        # make a request using the url
        response = client.get('/')


        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}The \
                         IndexView did not give the correct response code \
                         of 200.{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'expensense/index.html', 
                                f"{FAILURE_HEADER}The IndexView did not use \
                                    the correct template{FAILURE_FOOTER}")
        
    def test_index_view_rendering_using_reverse(self):
        """
        Test to check if the index page is being rendered using reverse
        function name
        """

        client = Client()

        response = client.get(reverse('index'))

        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}The \
                         IndexView did not give the correct response code \
                         of 200.{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'expensense/index.html', 
                                f"{FAILURE_HEADER}The IndexView did not use \
                                    the correct template{FAILURE_FOOTER}")

    def test_index_url_exists(self):
        """
        Test to check if index mapping exists in both project's urls.py and 
        app's urls.py
        """
        self.project_urls_module = importlib.import_module(
            'expensense_main.urls')
        index_mapping_exists = False

        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'index':
                    index_mapping_exists = True

        self.assertTrue(index_mapping_exists,
                        f"{FAILURE_HEADER}The index URL mapping does not \
                            exists{FAILURE_FOOTER}")
        self.assertEquals(reverse('expensense:index'), '/expensense/',
                          f"{FAILURE_HEADER}The index URL lookup failed.\
                            {FAILURE_FOOTER}")


class TemplateTest(TestCase):
    """
    Class to test the templates
    """

    def get_template(self, path_to_template):
        """
        Helper function to return the string representation of a template file
        """
        f = open(path_to_template, 'r')
        template_str = ""

        for line in f:
            template_str = f"{template_str}{line}"

        f.close()
        return template_str
    
    def test_base_template_exists(self):
        """
        Tests whether the base template exists
        """
        template_base_path = os.path.join(
            settings.TEMPLATE_DIR, 'expensense', 'base.html')
        self.assertTrue(os.path.exists(template_base_path),
                        f"{FAILURE_HEADER}No base.html template found in the \
                            templates/expensense directory.{FAILURE_FOOTER}")
    
    def test_index_template_exists(self):
        """
        Test whether the index template exists
        """
        template_base_path = os.path.join(
            settings.TEMPLATE_DIR, 'expensense', 'index.html')
        self.assertTrue(os.path.exists(template_base_path),
                        f"{FAILURE_HEADER}No index.html template found in the \
                            templates/expensense directory.{FAILURE_FOOTER}")

class RegisterStep1Test(TestCase):
    """
    Class to test registration step-1
    """
    def setUp(self):
        """
        Setup of a client to make requests
        """
        self.client = Client()

    def test_get_method(self):
        """
        Test the get method of the class
        """
        response = self.client.get(reverse('expensense:registration_step1'))
         

        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}The \
                         response code for getting the register Step1 is not \
                         200{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'expensense/register_step_1.html', 
                                f"{FAILURE_HEADER}The Template used is \
                                    register step-1 isnot the \
                                        expensense/register_step_1.html \
                                        specefied{FAILURE_FOOTER}")
        self.assertIsInstance(response.context['form'], Step1Form, 
                              f"{FAILURE_HEADER}The form used not the \
                                Step1Form{FAILURE_FOOTER}")

    # def test_post_method_valid_data(self):
    #     """
    #     Test to check post method with valid data
    #     """
    #     data = {'username': 'tester',
    #             'email': 'test@test.com',
    #             'password': 'test@123',
    #             'first_name': 'first_name',
    #             'last_name': 'last_name',
    #             'role':'ADM'}
    #     signature_file = SimpleUploadedFile("signature.jpg", b"file_content", content_type="image/jpeg")
    #     response = self.client.post(reverse('expensense:registration_step1'), data, files = {'signature': signature_file})

    #     self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}The \
    #                      post method is not posting the correct redirecting \
    #                      status code{FAILURE_FOOTER}")
    #     self.assertRedirects(response=response, expected_url=reverse('expensense:registration_step2'),
    #                          msg_prefix=f"{FAILURE_HEADER}The post method is not \
    #                             redirecting to the correct url{FAILURE_FOOTER}")
    #     self.assertEqual(self.client.session['step1_data'], data, 
    #                      f"{FAILURE_HEADER}The session data is not being \
    #                         stored correctly{FAILURE_FOOTER}")

    def test_post_method_invalid_data(self):
        """
        Test to check post method with invalid data
        """
        data = {'username': 'tester',
                'email': 'test@test.com',
                'password': 'test@123',
                'first_name': 'first_name',
                'last_name': 'last_name',
                'role':'APM'}
        response = self.client.post(reverse('expensense:registration_step1'), data)

        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER} \
                         The form is not giving the correct response \
                         code{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'expensense/register_step_1.html',
                                 f"{FAILURE_HEADER}The template used is not \
                                    the expensense/register_step_1.html\
                                        {FAILURE_FOOTER}")
        self.assertIsInstance(response.context['form'], Step1Form, 
                              f"{FAILURE_HEADER}The form is not an instance \
                                of Step-1 form{FAILURE_FOOTER}")
        form = response.context['form']
        self.assertFalse(form.is_valid(), f"{FAILURE_HEADER} The form is \
                         becoming valid for invalid input{FAILURE_FOOTER}")

        # Make sure session data was not stored
        self.assertNotIn('step1_data', self.client.session, 
                         f"{FAILURE_HEADER}The session data is being stored \
                            for invalid form inputs{FAILURE_FOOTER}")

class Step1FormTestCase(TestCase):
    """ Class to test the register step-1 form"""
    # def test_valid_form(self):
    #     """ 
    #     Test with valid data
    #     """
    #     data = {
    #         'username': 'tester',
    #         'email': 'test@test.com',
    #         'password': 'test@123456',
    #         'first_name': 'first',
    #         'last_name': 'last',
    #         'role': 'ADM'
    #     }
    #     files = {
    #         'signature': SimpleUploadedFile('signature.jpeg', b"file_content", content_type="image/jpeg")
    #     }
    #     form = Step1Form(data=data, files=files)
    #     self.assertTrue(form.is_valid(), f"{FAILURE_HEADER}The form is \
    #                     treating some field as invalid{FAILURE_FOOTER}")

    def test_invalid_form(self):
        """
        Test for all invalid field inputs
        """
        data = {
            'username': '',
            'email': 'invalid-email',
            'password': 'short',
            'first_name': '',
            'last_name': '',
            'role': 'XYZ'  # Invalid role
        }
        files = {
            'signature': None
        }
        form = Step1Form(data=data, files=files)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 7, f"{FAILURE_HEADER}All 7 fields \
                         have invalid input{FAILURE_FOOTER}")

    def test_password_min_length(self):
        """
        Test for password length less than 8
        """
        data = {
            'username': 'tester',
            'email': 'test@test.com',
            'password': 'short',  # Password too short
            'first_name': 'first',
            'last_name': 'last',
            'role': 'ADM'
        }
        form = Step1Form(data=data)
        self.assertFalse(form.is_valid(), f"{FAILURE_HEADER}The form is \
                         valid even with short password{FAILURE_FOOTER}")
        self.assertIn('password', form.errors, f"{FAILURE_HEADER}The short \
                      password is being accepted{FAILURE_FOOTER}")

    def test_role_choices(self):
        """
        Test for invalid role
        """
        data = {
            'username': 'tester',
            'email': 'test@test.com',
            'password': 'test@123456',
            'first_name': 'first',
            'last_name': 'last',
            'role': 'XYZ'  # Invalid role
        }
        form = Step1Form(data=data)
        self.assertFalse(form.is_valid(), f"{FAILURE_HEADER}The form is still \
                         valid for invalid role{FAILURE_FOOTER}")
        self.assertIn('role', form.errors, f"{FAILURE_HEADER}The role is being \
                      treated as valid option{FAILURE_FOOTER}")


class RegistrationStep2ViewTestCase(TestCase):
    """
    Class to test Registration Step-2
    """
    def setUp(self):
        """ Method to set up client, company and team """
        self.client = Client()

    def setup_session_admin(self):
        """ Method to set up session data for Admin """
        session = self.client.session
        session['step1_data'] = {
            'username': 'testadmin',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'first_name': 'first',
            'last_name': 'last',
            'role': 'ADM',
            # 'signature': SimpleUploadedFile('signature.jpeg', b"file_content", content_type="image/jpeg")
        }
        session.save()
    
    def setup_session_manager(self):
        """ Method to set up session data for Manager """
        session = self.client.session
        session['step1_data'] = {
            'username': 'testmanager',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'first_name': 'first',
            'last_name': 'last',
            'role': 'MNG',
            # 'signature': SimpleUploadedFile('signature.jpeg', b"file_content", content_type="image/jpeg")
        }
        session.save()
    
    def setup_session_employee(self):
        """ Method to set up session data for Employee """
        session = self.client.session
        session['step1_data'] = {
            'username': 'testemployee',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'first_name': 'first',
            'last_name': 'last',
            'role': 'EMP',
            # 'signature': SimpleUploadedFile('signature.jpeg', b"file_content", content_type="image/jpeg")
        }
        session.save()
    
    def setup_session_invalid_role(self):
        """ Method to set up session data for invalid role """
        session = self.client.session
        session['step1_data'] = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'first_name': 'first',
            'last_name': 'last',
            'role': 'XYZ'
        }
        session.save()

    def test_get_method_admin(self):
        """ Method to test step-2 form for admin"""
        self.setup_session_admin()
        response = self.client.get(reverse('expensense:registration_step2'))

        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER} \
                         The response code is not 200{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'expensense/register_step_2.html', 
                                msg_prefix=f"{FAILURE_HEADER}The \
                                    expensense/register_step_2.html is not \
                                        used{FAILURE_FOOTER}")
        self.assertIsInstance(response.context['form'], Step2FormAdmin, f"\
                              {FAILURE_HEADER}The form is not an instance of \
                                Step2FormAdmin{FAILURE_FOOTER}")
    
    def test_get_method_manager(self):
        """ Method to test step-2 form for manager"""
        self.setup_session_manager()
        response = self.client.get(reverse('expensense:registration_step2'))

        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER} \
                         The response code is not 200{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'expensense/register_step_2.html', 
                                msg_prefix=f"{FAILURE_HEADER}The \
                                    expensense/register_step_2.html is not \
                                        used{FAILURE_FOOTER}")
        self.assertIsInstance(response.context['form'], Step2FormManager, f"\
                              {FAILURE_HEADER}The form is not an instance of \
                                Step2FormManager{FAILURE_FOOTER}")
    
    def test_get_method_employee(self):
        """ Method to test step-2 form for employee"""
        self.setup_session_employee()
        response = self.client.get(reverse('expensense:registration_step2'))

        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER} \
                         The response code is not 200{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'expensense/register_step_2.html', 
                                msg_prefix=f"{FAILURE_HEADER}The \
                                    expensense/register_step_2.html is not \
                                        used{FAILURE_FOOTER}")
        self.assertIsInstance(response.context['form'], Step2FormEmployee, f"\
                              {FAILURE_HEADER}The form is not an instance of \
                                Step2FormEmployee{FAILURE_FOOTER}")

    def test_get_method_invalid_role(self):
        """ Method to test step-2 form for employee"""
        self.setup_session_invalid_role()
        response = self.client.get(reverse('expensense:registration_step2'))

        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER} \
                         The response code is not 302{FAILURE_FOOTER}")

    # def test_post_method_valid_data_step2admin(self):
    #     """ Method to check for valid data in step-2 admin form"""
    #     self.setup_session_admin()
    #     data = {
    #         'company': 'Test Company',
    #         'company_budget': 1000.00
    #     }
    #     response = self.client.post(reverse('expensense:registration_step2'), data)
    #     user = User.objects.get(username='testadmin')

    #     self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}\
    #                      The status code is not 302{FAILURE_FOOTER}")
    #     self.assertRedirects(response, reverse('expensense:login'),
    #                          msg_prefix=f"{FAILURE_HEADER}The redirect is not\
    #                             to the login page{FAILURE_FOOTER}")
    #     self.assertEqual(user.company.company, 'Test Company', 
    #                      f"{FAILURE_HEADER}The company name is not the one \
    #                         in the data{FAILURE_FOOTER}")
    #     self.assertEqual(user.company.company_budget, 1000.00, 
    #                      f"{FAILURE_HEADER}The company budget is not the one \
    #                         in the data{FAILURE_FOOTER}")
    #     self.assertEqual(user.team.team_name, 'Admin', f"{FAILURE_HEADER}The \
    #                      team for admin is not Admin{FAILURE_FOOTER}")
    #     self.assertNotIn('step1_data', self.client.session, 
    #                      f"{FAILURE_HEADER}The session data is not being \
    #                         deleted{FAILURE_FOOTER}")
    
    # def test_post_method_valid_data_step2manager(self):
    #     """ Method to check for valid data in step-2 manager form"""
    #     self.company = Company.objects.create(company='Test Company', company_budget=1000.00)
    #     self.setup_session_manager()
    #     data = {
    #         'company': self.company.pk,
    #         'team_name': 'Test Team',
    #         'team_budget': 1000.00
    #     }
    #     response = self.client.post(reverse('expensense:registration_step2'), data)
    #     user = User.objects.get(username='testmanager')

    #     self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}\
    #                      The status code is not 302{FAILURE_FOOTER}")
    #     self.assertRedirects(response, reverse('expensense:login'),
    #                          msg_prefix=f"{FAILURE_HEADER}The redirect is not\
    #                             to the login page{FAILURE_FOOTER}")
    #     self.assertEqual(user.company.company, 'Test Company', 
    #                      f"{FAILURE_HEADER}The company name is not the one \
    #                         in the data{FAILURE_FOOTER}")
    #     self.assertEqual(user.team.team_budget, 1000.00, 
    #                      f"{FAILURE_HEADER}The company budget is not the one \
    #                         in the data{FAILURE_FOOTER}")
    #     self.assertEqual(user.team.team_name, 'Test Team', f"{FAILURE_HEADER}\
    #                      The team for manager is not Test Team{FAILURE_FOOTER}")
    #     self.assertNotIn('step1_data', self.client.session, 
    #                      f"{FAILURE_HEADER}The session data is not being \
    #                         deleted{FAILURE_FOOTER}")
    
    # def test_post_method_valid_data_step2employee(self):
    #     """ Method to check for valid data in step-2 employee form"""
    #     self.company = Company.objects.create(company='Test Company', company_budget=1000.00)
    #     self.team = Team.objects.create(team_name='Test Team', company=self.company, team_budget=500.00)
        
    #     self.setup_session_employee()
        
    #     data = {
    #         'company': self.company.pk,
    #         'team_name': self.team.pk
    #     }
        
    #     response = self.client.post(reverse('expensense:registration_step2'), data)
    #     user = User.objects.get(username='testemployee')

    #     self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}\
    #                      The status code is not 302{FAILURE_FOOTER}")
    #     self.assertRedirects(response, reverse('expensense:login'),
    #                          msg_prefix=f"{FAILURE_HEADER}The redirect is not\
    #                             to the login page{FAILURE_FOOTER}")
    #     self.assertEqual(user.company.company, 'Test Company', 
    #                      f"{FAILURE_HEADER}The company name is not the one \
    #                         in the data{FAILURE_FOOTER}")
    #     self.assertEqual(user.team.team_name, 'Test Team', f"{FAILURE_HEADER}\
    #                      The team for employee is not Test Team{FAILURE_FOOTER}")
    #     self.assertNotIn('step1_data', self.client.session, 
    #                      f"{FAILURE_HEADER}The session data is not being \
    #                         deleted{FAILURE_FOOTER}")

    def test_post_method_invalid_company_data_admin(self):
        """
        Test Case for invalid admin form for company
        """
        self.setup_session_admin()
        data = {
            'company': '',
            'company_budget': 1000.00
        }
        response = self.client.post(reverse('expensense:registration_step2'), data)

        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}\
                         Status code not 200{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'expensense/register_step_2.html', 
                                msg_prefix=f"{FAILURE_HEADER}\
                                    expensense/register_step_2.html is not \
                                        returned{FAILURE_FOOTER}")
        self.assertIsInstance(response.context['form'], Step2FormAdmin, 
                              f"{FAILURE_HEADER}the form is not Step2FormAdmin\
                                {FAILURE_FOOTER}")
        form = response.context['form']
        self.assertFalse(form.is_valid(), f"{FAILURE_HEADER} The form is \
                         becoming valid for invalid input{FAILURE_FOOTER}")
    
    def test_post_method_invalid_company_budget_data_admin(self):
        """
        Test Case for invalid admin form for company budget
        """
        self.setup_session_admin()
        data = {
            'company': 'Test Company',
            'company_budget': ''
        }
        response = self.client.post(reverse('expensense:registration_step2'), data)

        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}\
                         Status code not 200{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'expensense/register_step_2.html', 
                                msg_prefix=f"{FAILURE_HEADER}\
                                    expensense/register_step_2.html is not \
                                        returned{FAILURE_FOOTER}")
        self.assertIsInstance(response.context['form'], Step2FormAdmin, 
                              f"{FAILURE_HEADER}the form is not Step2FormAdmin\
                                {FAILURE_FOOTER}")
        form = response.context['form']
        self.assertFalse(form.is_valid(), f"{FAILURE_HEADER} The form is \
                         becoming valid for invalid input{FAILURE_FOOTER}")
    
    def test_post_method_invalid_company_budget_more_decimal_data_admin(self):
        """
        Test Case for invalid admin form for company budget with more than 2 decimal places
        """
        self.setup_session_admin()
        data = {
            'company': 'Test Company',
            'company_budget': 23.2344
        }
        response = self.client.post(reverse('expensense:registration_step2'), data)

        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}\
                         Status code not 200{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'expensense/register_step_2.html', 
                                msg_prefix=f"{FAILURE_HEADER}\
                                    expensense/register_step_2.html is not \
                                        returned{FAILURE_FOOTER}")
        self.assertIsInstance(response.context['form'], Step2FormAdmin, 
                              f"{FAILURE_HEADER}the form is not Step2FormAdmin\
                                {FAILURE_FOOTER}")
        form = response.context['form']
        self.assertFalse(form.is_valid(), f"{FAILURE_HEADER} The form is \
                         becoming valid for invalid input{FAILURE_FOOTER}")
    
    def test_post_method_invalid_team_name_data_step2manager(self):
        """ Method to check for invalid data in step-2 manager form"""
        self.company = Company.objects.create(company='Test Company', company_budget=1000.00)
        self.setup_session_manager()
        data = {
            'company': self.company.pk,
            'team_name': '',
            'team_budget': 1000.00
        }
        response = self.client.post(reverse('expensense:registration_step2'), data)
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}\
                         Status code not 200{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'expensense/register_step_2.html', 
                                msg_prefix=f"{FAILURE_HEADER}\
                                    expensense/register_step_2.html is not \
                                        returned{FAILURE_FOOTER}")
        self.assertIsInstance(response.context['form'], Step2FormManager, 
                              f"{FAILURE_HEADER}the form is not Step2FormManager\
                                {FAILURE_FOOTER}")
        form = response.context['form']
        self.assertFalse(form.is_valid(), f"{FAILURE_HEADER} The form is \
                         becoming valid for invalid input{FAILURE_FOOTER}")
    
    def test_post_method_invalid_team_budget_data_step2manager(self):
        """ Method to check for invalid data in step-2 manager form"""
        self.company = Company.objects.create(company='Test Company', company_budget=1000.00)
        self.setup_session_manager()
        data = {
            'company': self.company.pk,
            'team_name': 'Test Team',
            'team_budget': ''
        }
        response = self.client.post(reverse('expensense:registration_step2'), data)
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}\
                         Status code not 200{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'expensense/register_step_2.html', 
                                msg_prefix=f"{FAILURE_HEADER}\
                                    expensense/register_step_2.html is not \
                                        returned{FAILURE_FOOTER}")
        self.assertIsInstance(response.context['form'], Step2FormManager, 
                              f"{FAILURE_HEADER}the form is not Step2FormManager\
                                {FAILURE_FOOTER}")
        form = response.context['form']
        self.assertFalse(form.is_valid(), f"{FAILURE_HEADER} The form is \
                         becoming valid for invalid input{FAILURE_FOOTER}")
    
    def test_post_method_invalid_team_budget2_data_step2manager(self):
        """ Method to check for invalid data in step-2 manager form"""
        self.company = Company.objects.create(company='Test Company', company_budget=1000.00)
        self.setup_session_manager()
        data = {
            'company': self.company.pk,
            'team_name': 'Test Team',
            'team_budget': 100.8787
        }
        response = self.client.post(reverse('expensense:registration_step2'), data)
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}\
                         Status code not 200{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'expensense/register_step_2.html', 
                                msg_prefix=f"{FAILURE_HEADER}\
                                    expensense/register_step_2.html is not \
                                        returned{FAILURE_FOOTER}")
        self.assertIsInstance(response.context['form'], Step2FormManager, 
                              f"{FAILURE_HEADER}the form is not Step2FormManager\
                                {FAILURE_FOOTER}")
        form = response.context['form']
        self.assertFalse(form.is_valid(), f"{FAILURE_HEADER} The form is \
                         becoming valid for invalid input{FAILURE_FOOTER}")
    
    def test_post_method_invalid_company_data_step2employee(self):
        """ Method to check for invalid data in step-2 employee form"""
        self.company = Company.objects.create(company='Test Company', company_budget=1000.00)
        self.team = Team.objects.create(team_name='Test Team', company=self.company, team_budget=500.00)
        self.setup_session_employee()
        data = {
            'company': '',
            'team_name': 'Test Team',
        }
        response = self.client.post(reverse('expensense:registration_step2'), data)
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}\
                         Status code not 200{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'expensense/register_step_2.html', 
                                msg_prefix=f"{FAILURE_HEADER}\
                                    expensense/register_step_2.html is not \
                                        returned{FAILURE_FOOTER}")
        self.assertIsInstance(response.context['form'], Step2FormEmployee, 
                              f"{FAILURE_HEADER}the form is not \
                                Step2FormEmployee{FAILURE_FOOTER}")
        form = response.context['form']
        self.assertFalse(form.is_valid(), f"{FAILURE_HEADER} The form is \
                         becoming valid for invalid input{FAILURE_FOOTER}")
    
    def test_post_method_invalid_team_data_step2employee(self):
        """ Method to check for invalid data in step-2 employee form"""
        self.company = Company.objects.create(company='Test Company', company_budget=1000.00)
        self.team = Team.objects.create(team_name='Test Team', company=self.company, team_budget=500.00)
        self.setup_session_employee()
        data = {
            'company': self.company.pk,
            'team_name': 'Test Team',
        }
        response = self.client.post(reverse('expensense:registration_step2'), data)
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}\
                         Status code not 200{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'expensense/register_step_2.html', 
                                msg_prefix=f"{FAILURE_HEADER}\
                                    expensense/register_step_2.html is not \
                                        returned{FAILURE_FOOTER}")
        self.assertIsInstance(response.context['form'], Step2FormEmployee, 
                              f"{FAILURE_HEADER}the form is not \
                                Step2FormEmployee{FAILURE_FOOTER}")
        form = response.context['form']
        self.assertFalse(form.is_valid(), f"{FAILURE_HEADER} The form is \
                         becoming valid for invalid input{FAILURE_FOOTER}")

class TeamsViewTest(TestCase):
    """
    Class containg test cases for teams API 
    """
    def setUp(self):
        """ Method to set up the company teams object instances """
        self.client = Client()
        self.company = Company.objects.create(company='Test Company',
                                               company_budget=1000.00)
        self.team1 = Team.objects.create(company = self.company, 
                                         team_name='Team A')
        self.team2 = Team.objects.create(company = self.company, 
                                         team_name='Team B')

    def test_teams_view(self):
        """ Test case for valid company id"""
        data = {'comp_id': self.company.id}
        response = self.client.post(reverse('expensense:teams'), 
                                    data=json.dumps(data), 
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        expected_data = [
            {'id': self.team1.id, 'team_name': 'Team A'},
            {'id': self.team2.id, 'team_name': 'Team B'}
        ]
        self.assertEqual(json.loads(response.content), expected_data, 
                         f"{FAILURE_HEADER}API Response is not same\
                            {FAILURE_FOOTER}")

    def test_teams_view_invalid_company_id(self):
        """ Test case for invalid company id"""
        invalid_company_id = 999
        data = {'comp_id': invalid_company_id}
        response = self.client.post(reverse('expensense:teams'), 
                                    data=json.dumps(data), 
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}API \
                         Response code is not 200{FAILURE_FOOTER}")
        self.assertEqual(json.loads(response.content), [], f"{FAILURE_HEADER}\
                         API response is not empty{FAILURE_FOOTER}")


class LoginViewTestCase(TestCase):
    """
    Class for LoginView Test Cases
    """
    def setUp(self):
        """ Method to set up the client, user and login_url """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.login_url = reverse('expensense:login')

    def test_get_method(self):
        """ GET method test """
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}API \
                         Response code is not 200{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'expensense/login.html')

    def test_post_method_valid_credentials(self):
        """ Valid credential Post test"""
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.login_url, data=data)

        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}API \
                         Response code is not 302{FAILURE_FOOTER}")
        self.assertRedirects(response, reverse('expensense:dashboard'), 
                             msg_prefix= f"{FAILURE_HEADER} the redictection \
                                is not to dashboard{FAILURE_FOOTER}")

    def test_post_method_inactive_user(self):
        """Inactive user login test"""
        self.user.is_active = False
        self.user.save()

        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.login_url, data=data)

        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}API \
                         Response code is not 200{FAILURE_FOOTER}")
        self.assertEqual(response.content.decode(), 'Invalid login details supplied', 
                         f"{FAILURE_HEADER}HTTP Response is not Invalid login details\
                            {FAILURE_FOOTER}")

    @patch('django.contrib.auth.authenticate')
    def test_post_method_invalid_credentials(self, mock_authenticate):
        """ Invalid credentials login test"""
        mock_authenticate.return_value = None

        data = {'username': 'invaliduser', 'password': 'invalidpassword'}
        response = self.client.post(self.login_url, data=data)

        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}API \
                         Response code is not 200{FAILURE_FOOTER}")
        self.assertEqual(response.content.decode(), 'Invalid login details supplied', 
                         f"{FAILURE_HEADER}HTTP Response is not Invalid login details\
                            {FAILURE_FOOTER}")

class LogoutViewTest(TestCase):
    """ Class for logout test cases """
    def setUp(self):
        """ Method to setup the test cases"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.login_url = reverse('expensense:login')
        self.logout_url = reverse('expensense:logout')

    def test_get_method_logged_in_user(self):
        """ Test for logged in user """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.logout_url)

        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}\
                         Response code is not 302{FAILURE_FOOTER}")
        self.assertRedirects(response, reverse('expensense:index'), 
                             msg_prefix= f"{FAILURE_HEADER} the redictection \
                                is not to homepage{FAILURE_FOOTER}")

    def test_get_method_logged_out_user(self):
        """ Test for logged out user """
        response = self.client.get(self.logout_url)

        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}\
                         Response code is not 302{FAILURE_FOOTER}")
        self.assertRedirects(response, '/expensense/login/?next=/expensense/logout/', 
                             msg_prefix= f"{FAILURE_HEADER} the redictection \
                                is not to login{FAILURE_FOOTER}")