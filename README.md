# Restaurant Project - Django Exploration

This is a simple Django project created for learning and exploration purposes. It focuses on restaurant management and allows you to model various aspects like cities, restaurants, food categories, dishes, and user ratings for both restaurants and dishes.

## Screenshots

![Image 2](/screenshots/img2.png)
![Image 3](/screenshots/img3.png)
![Image 1](/screenshots/img1.png)

## Installation

1. **Install Python 3.12.3 using uv**

   [Refer the page](https://docs.astral.sh/uv/getting-started/installation)

2. **Fetch the project files from GitHub**

   ```bash
   git clone https://github.com/anand-jaiswal-IN/restaurantlookup.git
   ```

3. **Navigate to the project directory**

   ```bash
   cd restrauntlookup
   ```

4. **Install the required packages**

   ```bash
   uv sync
   ```

## Usage

1. **Set up the project environment**

   Follow the installation steps above to set up your virtual environment and install dependencies.

2. **Set up environment variables in the project**

   In the project you find a file `.env.sample`, rename this file into `.env` and change the variables values into instruted.

   if you want to use `sqlite3` as database then go to `restraurantlookup/settings.py` and search for `DATABASES` comment the desired values.

3. **Migrate the models**

   Apply the database migrations to create the necessary tables.

   ```bash
   uv run manage.py makemigrations && uv run manage.py migrate
   ```

4. **Run static files command**

   ```bash
   uv run manage.py collectstatic
   ```

5. **Use the Django admin interface**

   Create a superuser to access the Django admin interface.

   ```bash
   uv run manage.py createsuperuser
   ```

6. **Run the development server**

   Start the Django development server to see your project in action.

   ```bash
   uv run manage.py runserver
   ```

Navigate to `http://127.0.0.1:8000/` to view website and create users and restaurants.

Navigate to `http://127.0.0.1:8000/admin/` and log in with your superuser credentials to manage your models.
