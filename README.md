# Restaurant Project - Django Exploration

This is a simple Django project created for learning and exploration purposes. It focuses on restaurant management and allows you to model various aspects like cities, restaurants, food categories, dishes, and user ratings for both restaurants and dishes.

## Installation

1. **Install Python 3**

   Download and install Python 3 from the [official site](https://www.python.org/).

2. **Install `virtualenv` globally**

   ```bash
   pip install virtualenv
   ```

3. **Create a virtual environment**

   Navigate to your desired folder and create a virtual environment named `django`.

   ```bash
   virtualenv django
   ```

4. **Activate the virtual environment**

   - On Windows:

     ```bash
     django\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source django/bin/activate
     ```

5. **Fetch the project files from GitHub**

   ```bash
   git clone https://github.com/anand-jaiswal-IN/firstDjangoProject
   ```

6. **Navigate to the project directory**

   ```bash
   cd firstDjangoProject
   ```

7. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Models

The project includes the following models:

- **City:** Represents a city where restaurants can be located.
- **Restaurant:** Represents a restaurant with attributes like name, address, and city.
- **Food_category:** Classifies the type of cuisine offered by a dish (e.g., Italian, Mexican).
- **Dish:** Represents a dish offered by a restaurant with a name, description, and food category.
- **Rating_restaurant:** Stores user ratings for a specific restaurant.
- **Rating_dish:** Stores user ratings for a specific dish.

## Usage

1. **Set up the project environment**

   Follow the installation steps above to set up your virtual environment and install dependencies.

2. **Migrate the models**

   Apply the database migrations to create the necessary tables.

   ```bash
   python manage.py migrate
   ```

3. **Run the development server**

   Start the Django development server to see your project in action.

   ```bash
   python manage.py runserver
   ```

4. **Use the Django admin interface**

   Create a superuser to access the Django admin interface.

   ```bash
   python manage.py createsuperuser
   ```

Navigate to `http://127.0.0.1:8000/admin` and log in with your superuser credentials to manage your models.