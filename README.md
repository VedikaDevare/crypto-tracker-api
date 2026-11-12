# Crypto Tracker API

A cryptocurrency tracking REST API built with **Python and FastAPI**. It retrieves live cryptocurrency prices using the CoinGecko API, stores price snapshots, tracks price changes, and allows authenticated users to manage personal watchlists.

## Features

- **Live Cryptocurrency Prices:** Fetch current USD prices for Bitcoin, Ethereum, and Solana.
- **Price History:** Store and retrieve historical price snapshots using SQLite.
- **Price Change:** Calculate absolute and percentage price changes using the two latest snapshots.
- **User Authentication:** Register and log in with securely hashed passwords.
- **JWT Authentication:** Protect endpoints using JSON Web Tokens.
- **Personal Watchlists:** Add, view, and remove cryptocurrencies from a user's watchlist.
- **Input Validation:** Validate request and response data using Pydantic.
- **Automated Testing:** Test API functionality using Pytest and FastAPI TestClient.
- **API Documentation:** Interactive Swagger UI documentation.

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- HTTPX
- CoinGecko API
- JWT Authentication
- pwdlib (Argon2 password hashing)
- Pytest
- Git and GitHub
- Render

## Supported Cryptocurrencies

| Coin ID | Cryptocurrency |
|---|---|
| bitcoin | Bitcoin |
| ethereum | Ethereum |
| solana | Solana |

## API Endpoints

### General

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/docs` | Interactive API documentation |

### Cryptocurrency

| Method | Endpoint | Description |
|---|---|---|
| GET | `/coins/{coin_id}` | Fetch current price and save a snapshot |
| GET | `/coins/{coin_id}/history` | Retrieve price history |
| GET | `/coins/{coin_id}/change` | Calculate price change |

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Register a new user |
| POST | `/login` | Log in and receive a JWT |
| GET | `/me` | Retrieve the authenticated user's details |

### Watchlist

| Method | Endpoint | Description |
|---|---|---|
| POST | `/watchlist` | Add a cryptocurrency |
| GET | `/watchlist` | View the user's watchlist |
| DELETE | `/watchlist/{coin_id}` | Remove a cryptocurrency |

Protected endpoints require a valid Bearer token.

## Project Structure

```text
crypto_tracker/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── security.py
├── requirements.txt
├── .gitignore
│
├── routes/
│   ├── __init__.py
│   ├── coins.py
│   ├── users.py
│   └── watchlist.py
│
└── tests/
    ├── conftest.py
    └── test_main.py
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/VedikaDevare/crypto-tracker-api.git
cd crypto-tracker-api
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Set these environment variables before running the application:

```text
SECRET_KEY=your_secure_jwt_secret
COINGECKO_API_KEY=your_coingecko_demo_api_key
```

Never commit real API keys or secret values to GitHub.

### 5. Run the application

```bash
uvicorn main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

Open the interactive documentation at:

`http://127.0.0.1:8000/docs`

## Running Tests

Run the automated test suite using:

```bash
pytest -v
```

The project includes tests for health checks, cryptocurrency endpoints, authentication, input validation, and watchlist operations.

## Live Deployment

The API is deployed on Render:

**Base URL:**  
https://crypto-tracker-api-x48k.onrender.com

**API Documentation:**  
https://crypto-tracker-api-x48k.onrender.com/docs

Note: The deployed application uses SQLite. On hosting platforms with ephemeral filesystems, local database changes may not persist across restarts or redeployments. Persistent storage or a managed database is recommended for long-term production use.

## Future Improvements

- Build a simple HTML frontend.
- Add more cryptocurrency options.
- Introduce caching to reduce external API requests.
- Use a persistent production database.
- Add more advanced price analytics.

## Author

**Vedika Devare**

Electronics and Telecommunication Engineering Student

GitHub: [VedikaDevare](https://github.com/VedikaDevare)

---

*Developed as a learning and portfolio project to practice Python backend development, REST APIs, databases, authentication, testing, and deployment.*


## Frontend

A simple HTML and JavaScript frontend connected to the FastAPI backend.

### Features
- Displays live Bitcoin, Ethereum, and Solana prices.
- User login using JWT authentication.
- Add coins to a personal watchlist.
- View saved watchlist coins.
- Remove coins from the watchlist.
- Displays API error messages.

### How to use
1. Open `frontend/index.html` in a browser.
2. Log in using a registered username and password.
3. View live cryptocurrency prices.
4. Add, view, and remove coins from your watchlist.

The frontend communicates with the deployed FastAPI backend hosted on Render.
