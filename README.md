# CS50W Commerce
A web-based e-commerce site built using Django, HTML and CSS (with Bootstrap). This project was created as part of Harvard’s CS50 Web Programming with Python and JavaScript course.

## Features
- Create a listing with a base price
- Bid on items of other users
- Add listings to your watchlist
- Comment on listings
- Edit listing descriptions
- Close a listing

## Getting Started
Follow the steps below to get this project running on your local machine.

### Prerequisites
- Python 3.6+
- pip
- Git
- A web browser

### Installation

1. **Clone the Repository**
   
git clone https://github.com/ruissouw/cs50w-commerce.git

cd cs50w-mail

2. **Create a Virtual Environment**
   
python -m venv env

3. **Activate the Virtual Environment**
   
On macOS/Linux:

source env/bin/activate

On Windows:

env\Scripts\activate

4. **Install Dependencies**
   
pip install -r requirements.txt

5. **Apply Migrations**
   
python manage.py migrate

6. **Run the Development Server**
   
python manage.py runserver

7. **Open the App in Your Browser**
    
Visit http://127.0.0.1:8000/ to start using the application.
