## Project Name

English vocabulary

## Description

The English Vocabulary is a straightforward Django application created to assist users in storing and organizing their
vocabulary while studying or learning new languages. Whether you’re a language enthusiast, a student, or simply looking
to expand your word bank, this backend offers a convenient solution for saving and managing words. It’s built using
Django, incorporates OAuth2 authentication, utilizes the Django Rest Framework (DRF), and integrates with Swagger.

## Installation

1. **Prerequisites:**
    - Make sure you have Python and pip installed.
    - Create a virtual environment (optional but recommended).

2. **Clone the Repository:**
    ```
    git clone https://github.com/ManhTuongNguyen/EnglishVocabulary.git
    cd EnglishVocabulary
    ```

3. **Install Dependencies:**
    ```
    pip install -r requirements.txt
    ```

4. **Database Setup:**
    - Configure your database settings in settings.py.
    - Run migrations:
        ```
        python manage.py makemigrations
        python manage.py migrate
        ```
5. **OAuth2 Configuration:**

   Set up OAuth2 authentication using django-oauth-toolkit. Refer to the official documentation for detailed
   instructions.

6. **Setting up the `.env` file**
    - Begin by creating a `.env` file and placing it in the root directory of the project.
    - Configure the `.env` file based on the settings provided in the `.env.example` file.

## Usage

To run your project locally:

```
python manage.py runserver
```

Access the Swagger documentation at `http://127.0.0.1:8000/api/schema/swagger-ui/`.

## Acknowledgments

1. **Translator Package**

   The [translator package](https://github.com/uliontse/translators) plays a crucial role in my project by enabling seamless translation capabilities. I express my
   gratitude to the developers who contributed to this package.

2. **Dictionary API (dictionaryapi.dev)**
   
   I extend my appreciation to the creators of the Dictionary API provided by api.dictionaryapi.dev. This API allows me
   to retrieve phonetics, and other language-related data.
   functionality.

   If you’d like to explore the API further, you can visit [their official documentation](https://dictionaryapi.dev/).