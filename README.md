
# DishBoard - Restaurant and Menu Management System

## Project Description

DishBoard is a management system for restaurants, including restaurant details, opening hours, and menus. The system provides an API interface for easy interaction with the data.

### Key Features:
- Manage restaurants (add, edit, view, and delete).
- Manage restaurant opening hours.
- Manage menu categories.
- Add, edit, and delete menu items.

---

## Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/razmazlih/DishBoard.git
   cd DishBoard
   ```

2. **Install Dependencies**  
   Make sure to use a virtual environment or a similar environment management tool.  
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**  
   Create a `.env` file in the root directory and configure the following:
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1
   CORS_ALLOWED_ORIGINS=http://127.0.0.1:8000
   ```

4. **Apply Migrations**  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser**  
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Server**  
   ```bash
   python manage.py runserver
   ```

---

## Usage

### API Endpoints

The system provides various API endpoints for managing restaurants, opening hours, and menus. Below are some examples:

#### Restaurants
- **Get all restaurants**: `GET /info/`
- **Create a new restaurant**: `POST /info/`
  ```json
  {
      "name": "Restaurant Name",
      "city": "City",
      "address": "Address"
  }
  ```
- **Get a single restaurant**: `GET /info/{id}/`
- **Update restaurant details**: `PATCH /info/{id}/`
  ```json
  {
      "name": "Updated Name",
      "city": "Updated City",
      "address": "Updated Address"
  }
  ```

#### Opening Hours
- **Get opening hours**: `GET /opening-houers/?restaurant_id={restaurant_id}`
- **Update opening hours**: `PATCH /opening-houers/{id}/`
  ```json
  {
      "opening_time": "10:00",
      "closing_time": "22:00",
      "is_open": true
  }
  ```

#### Menu
- **Get categories**: `GET /category/?restaurant_id={restaurant_id}`
- **Create a new category**: `POST /category/`
  ```json
  {
      "name": "Starters",
      "restaurant": 1
  }
  ```
- **Get a single item**: `GET /item/{id}/`
- **Create a new item**: `POST /item/`
  ```json
  {
      "category": 3,
      "name": "Dish Name",
      "price": "12.50",
      "description": "Delicious dish description"
  }
  ```

---

## Docker Setup

DishBoard is fully containerized using Docker and Docker Compose.

### Prerequisites
- Ensure Docker and Docker Compose are installed on your machine.

### Steps to Run with Docker Compose
1. **Create a `.env` file**  
   Configure the following environment variables in the `.env` file:
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1
   CORS_ALLOWED_ORIGINS=http://127.0.0.1:8000
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   POSTGRES_DB=your_db_name
   ```

2. **Build and Start Services**  
   Run the following command to start the services:
   ```bash
   docker-compose up --build
   ```

3. **Access the Application**  
   - The backend API will be available at `http://127.0.0.1:8002`.
   - The PostgreSQL database will be available at `localhost:5432`.

---

## Contribution

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m "Add feature"`.
4. Push the branch: `git push origin feature-name`.
5. Submit a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

For any questions or suggestions, feel free to reach out at:
- Linkedin: [Raz Mazlih](https://www.linkedin.com/in/raz-mazlih)
- GitHub: [razmazlih](https://github.com/razmazlih)
