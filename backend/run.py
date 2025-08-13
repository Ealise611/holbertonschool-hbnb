# How to use:

#  USE_TEST_DB=true python3 run.py      Run with test database
#  python3 run.py                       Run with development database (normal):

import os
from app import create_app

# Check if we're in testing mode
config_name = "TestingConfig" if os.getenv("USE_TEST_DB") else "DevelopmentConfig"

app = create_app(config_name)

if __name__ == "__main__":
    db_type = "TEST" if os.getenv("USE_TEST_DB") else "DEVELOPMENT"
    print(f" Starting HBnB API with {db_type} database...")
    app.run(host="0.0.0.0", debug=True, port=5000)
