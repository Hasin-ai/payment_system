# Payment Gateway System

A secure and scalable payment gateway system that integrates with SSLCommerz for payment processing and PayPal for payouts.

## Features

- User authentication and authorization
- Multi-currency support with real-time exchange rates
- Secure payment processing via SSLCommerz
- Payouts via PayPal
- Admin dashboard for transaction management
- RESTful API with JWT authentication
- Rate limiting and request validation

## Prerequisites

- Python 3.8+
- PostgreSQL
- SSLCommerz account
- PayPal Developer account

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/payment-gateway.git
   cd payment-gateway
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example` and update the values:
   ```bash
   cp .env.example .env
   ```

5. Set up the database:
   ```bash
   alembic upgrade head
   ```

## Running the Application

1. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Start the Celery worker (in a separate terminal):
   ```bash
   celery -A app.worker.celery_app worker --loglevel=info
   ```

3. Access the API documentation at: http://localhost:8000/docs

## API Endpoints

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token
- `GET /api/v1/users/me` - Get current user info
- `POST /api/v1/payment/initiate` - Initiate a payment
- `POST /api/v1/payment/ipn` - SSLCommerz IPN handler
- `GET /api/v1/transactions` - Get user transactions
- `GET /api/v1/admin/config` - Get admin configuration (admin only)

## Environment Variables

See `.env.example` for all available environment variables.

## Testing

Run the test suite with:

```bash
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
