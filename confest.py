# # conftest.py

# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# from database import Base  # Assuming you have defined the Base in your app.models module

# TEST_DATABASE_URL = "postgresql://postgres:556677@localhost:5432/test_employee_db"
# #headers = {"Authorization": f"Bearer {access_token}"}
# @pytest.fixture(scope="function")
# def test_db_session():
#     engine = create_engine(TEST_DATABASE_URL)
#     Base.metadata.create_all(bind=engine)
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     session = SessionLocal()

#     # Yield the session for the test function to use
#     yield session

#     # Clean up after the test by rolling back any changes and closing the session
#     session.rollback()
#     session.close()