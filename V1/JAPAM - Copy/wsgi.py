import os
from app import create_app

# Default to development if not set in environment
env = os.getenv("FLASK_ENV", "development" if __name__ == "__main__" else "production")
app = create_app(env)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
