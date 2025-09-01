from app import app

# Vercel needs this for serverless deployment
if __name__ == "__main__":
    app.run()