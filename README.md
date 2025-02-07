# fb-del-callback

POC project for testing app deletion callback endpoint from Facebook.

## Prerequisites

- Python 3.12 or higher
- `uv` (Python package manager)

## Setup

1. **Clone the repository:**

    ```sh
    git clone <repository-url>
    cd fb-del-callback
    ```

2. **Create and activate a virtual environment:**

    ```sh
    uv sync # syncs the virtual environment with the dependencies
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Create a `.env` file in the project root and add the following environment variables:**

    ```env
    BASE_URL=http://localhost:5000
    APP_ID=your-facebook-app-id
    APP_VERSION=v10.0
    APP_SECRET=your-facebook-app-secret
    ```

## Running the Application

1. **Start the Flask application:**

    ```sh
    python app.py
    ```

2. **Access the application:**

    Open your web browser and navigate to `http://localhost:5000`.

## Endpoints

- **GET `/`**: Home endpoint.
- **GET `/login`**: Login endpoint that renders the Facebook login page.
- **POST `/facebook_callback`**: Endpoint to handle Facebook callback.
- **GET `/deletion?id=<id>`**: Endpoint to handle deletion requests.

## Templates

- **`login.html`**: Renders the Facebook login snippet.
- **`deletion_status.html`**: Renders the deletion status message.
- **`error.html`**: Renders an error message.

## Project Structure

```
fb-del-callback/
│
├── app.py
├── .env
├── .python-version
├── pyproject.toml
├── requirements.txt
└── templates/
    ├── login.html
    ├── deletion_status.html
    └── error.html
```

## License

This project is licensed under the MIT License. See the `LICENSE.txt` file for details.