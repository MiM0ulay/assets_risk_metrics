import os
import sys

# Add the src directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Import the app
import app

# Run the app
if __name__ == "__main__":
    app.main()
