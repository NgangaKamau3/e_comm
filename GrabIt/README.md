# GrabIt E-Commerce Platform

A Flask-based e-commerce platform with responsive design and modern features.

## Features

- Product browsing by categories
- Shopping cart functionality
- User authentication
- Product management
- Responsive design
- Image upload capability

## Tech Stack

- Python 3.x
- Flask
- MySQL
- Bootstrap 5
- JavaScript

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/GrabIt.git
cd GrabIt
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy environment variables:
```bash
cp .env.example .env
```

5. Configure your .env file with appropriate values

6. Initialize the database:
```bash
mysql -u root < schema.sql
```

7. Run the application:
```bash
flask run
```

## Project Structure

```
GrabIt/
├── static/
│   ├── images/
│   ├── css/
│   └── js/
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── product_detail.html
│   └── ...
├── app.py
├── schema.sql
├── requirements.txt
└── README.md
```

## Configuration

Configure your environment variables in `.env`:
- `DB_HOST`: Database host
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_NAME`: Database name
- `SECRET_KEY`: Flask secret key

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details