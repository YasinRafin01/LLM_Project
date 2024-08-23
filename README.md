# Property Information Rewriter

This Django CLI application rewrites property information using Ollama and stores summaries in a database.

## Features

- Rewrites property titles and descriptions using an Ollama model
- Generates summaries for properties
- Stores information in a PostgreSQL database using Django ORM

## Prerequisites

- Python 3.8+
- Django 3.2+
- PostgreSQL
- Ollama
-  gemma2:2b

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/YasinRafin01/LLM_Project.git
   ```
2. Create a virtual environment and activate it:
   ```
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```
3. Install the required packages:
   ```
    pip install -r requirements.txt
   ```
4. Inside LLM_Project/property_manager/settings.py make sure to set the path with Django project path in the desktop like below:
   ```
   sys.path.append('Django_project_path')
   ```
5. Set up the PostgreSQL database and update the `DATABASES` configuration in `settings.py` this set up should contain the similar 
   database used in Django.
   
   For Django Database configuration following steps required
   - Open Linux/Mac Terminal and type
     ```
     nano ~/.pg_service.conf
     ```
   - Then put the following configuration, Save and exit
     ```
     [my_service]
     host=localhost
     user=postgres
     dbname= django_database_name
     port= your_port_number
     password= your_password
     ```
6. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
   
## Usage

1. Ensure Ollama is running and the desired model is available.

2. Run the CLI command to rewrite property information:
   ```
   python manage.py rewrite_properties
   ```

## Project Structure

- `properties/`: Django app containing models and management commands
- `properties/models.py`: Defines the Property and PropertySummary models
- `properties/management/commands/`: Contains the custom management commands

## Ollama Integration

This project uses Ollama to rewrite property information and generate summaries. Make sure you have Ollama installed and running with your chosen model.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
