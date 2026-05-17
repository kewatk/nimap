from app.database import create_tables
from app.models import associations, client, project, user 

if __name__ == "__main__":
    create_tables()