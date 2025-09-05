# Prediction Service API

# ![FAST API](https://i.imgur.com/yIzsPnj.png)

This project aims to develop a robust and secure FastAPI-based API that exposes a sophisticated machine learning model for predicting loan eligibility. The API integrates advanced security mechanisms, user authentication, and administrative functionalities, ensuring seamless operation and data protection. Designed with scalability in mind, it is optimized for deployment on Azure, leveraging Terraform for infrastructure automation. The system also includes comprehensive logging, monitoring, and administrative tools to support efficient management and scalability in a production environment

---

## Project Objectives

- **Model Exposure**  
  - Provide an endpoint to predict loan eligibility.
  - Provide an endpoints to authenticate users and admin.
  - Provide an endpoint to sync django and fastapi app.
  - Provide an endpoint to view loan request history.
  - Provide an endpoints to view list of users and admins.


- **API Security**  
  Implement JWT and OAuth2 authentication to secure endpoint access.

- **User Management**  
  - Only an administrator can create a new user account.
  - Users can request loans.
  - Users can change their password.

- **Request Logging**  
  Log all loan requests in a database for statistical analysis.

---

## Technologies Used

- **Language:** Python  
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)  
- **Database:** MSSQL (Azure) & SQLModel (built on SQLAlchemy and Pydantic) (Local)  
- **Authentication:** JWT (JSON Web Token) with OAuth2  
- **Docker:** Application containerization  
- **Azure:**  
  - Azure Container Instance to host the API  
  - Azure SQL Database (optional, for data persistence)  
- **Terraform** *(optional):* For Infrastructure as Code

---

## Key Features

- **Authentication & Security**  
  - JWT tokens with expiration  
  - Password hashing and salting  
  - Role-based access control (Admin, User)

- **API Endpoints**

| Method | URL                | Description                                                    | Access     |
| ------ | ------------------ | -------------------------------------------------------------- | ---------- |
| POST   | /auth/login        | Login and retrieve token                                       | All        |
| POST   | /auth/activation   | Account activation and password change                         | User       |
| POST   | /auth/logout       | Logout                                                         | User       |
| GET    | /loans/predict     | Predict loan eligibility                                       | User       |
| POST   | /loans/request     | Submit a loan request                                          | User       |
| GET    | /loans/history     | Retrieve loan request history                                  | User       |
| GET    | /admin/users       | List all users                                                 | Admin      |
| POST   | /admin/users       | Create a new user                                              | Admin      |

- **Database Structure**

  - **Table `users`:** Stores user data (email, hashed password, role, activation status, etc.).  
  - **Table `loan_requests`:** Stores loan request details including status and the requestor’s identifier.

---

## Installation and Setup

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt

2. **Database Configuration**

Initialize and manage database migrations with Alembic:

```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

3. **Seed the Database**
Run the script to populate the database:

```bash
python populate_db.py
```

4. **Run Tests**
```bash
python tests/test_app.py
```

5. **Environment Setup**

Create a `.env` file at the root of the project and define the required environment variables:

- `DATABASE_URL`
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- (Additional variables as needed, e.g., `DEBUG`, `ALLOWED_HOSTS`)


###  Running the API
To run the API locally:

```bash
uvicorn main:app --reload
```

This will start the development server accessible at http://127.0.0.1:8000.


## Deployment on Azure

The deployment is automated via the `deploy.sh` script, which performs the following steps:

1. **Prerequisite Checks**

    - Verifies that the Azure CLI (`az`) is installed.
    - Confirms the existence of the `.env` file and loads its variables.

2. **Azure Authentication**

    - Checks that the user is logged in using `az login`.

3. **Retrieve Azure Container Registry (ACR) Credentials**

4. **Remove Existing Container (if any)**
The script deletes any existing container before deploying a new one.

5. **Deploy a New Container**
The container is deployed using the Docker image stored in ACR with the proper environment configuration.

Run the script from the terminal:

```bash
[deploy.sh](http://_vscodecontentref_/0)
```

Ensure the script has executable permissions. If not, run:

```bash
chmod +x [deploy.sh](http://_vscodecontentref_/1)
```

## Docker & Docker Compose

A `Dockerfile` is provided to build the Docker image for the application. A `docker-compose.yaml` file is also available if you prefer to orchestrate services using Docker Compose.

```
.
├── Dockerfile
├── [docker-compose.yaml](http://_vscodecontentref_/2)
├── [deploy.sh](http://_vscodecontentref_/3)
├── [requirements.txt](http://_vscodecontentref_/4)
├── [readme.md](http://_vscodecontentref_/5)
├── [main.py](http://_vscodecontentref_/6)
├── [populate_db.py](http://_vscodecontentref_/7)
├── [test_app.py](http://_vscodecontentref_/8)
├── alembic/
│   ├── env.py
│   └── versions/
├── core/
├── data/
├── db/
├── endpoints/
├── models/
├── schemas/
├── startpoint/
├── terraform/
└── utils/
```

- **Core & Utils:** Contains configuration settings, password management, and JWT handlers.
- **Endpoints:** Groups the route handlers for authentication, loan processing, administration, etc.
- **DB / Alembic:** Manages database configuration and migrations.
- **Terraform:** Contains the files for optional Infrastructure as Code deployments.

## Advanced Deployment

The project also supports advanced deployment approaches:

- **Level 1:** Manual deployment via the Azure portal (using ACI for both the FastAPI and Django applications, and Azure SQL Database).
- **Level 2:** Automation via the deploy.sh script using the Azure CLI.
- **[Bonus] Level 3:** Use Terraform for declarative infrastructure management.


## Conclusion

This project implements a secure API that exposes a loan eligibility prediction model. By automating deployment with tools like Docker, the Azure CLI, and optionally Terraform, it provides a comprehensive solution from local development to production deployment.

For any questions or contributions, please refer to the project documentation and ensure secure management of sensitive information using the `.env` file. 

## Contributing

Contributions are welcome!  
1. **Fork the Project**  
2. **Create a Feature Branch**: `git checkout -b feature/new-feature`  
3. **Commit Your Changes**  
4. **Push to Your Branch**: `git push origin feature/new-feature`  
5. **Open a Pull Request**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author

This project was completed by [Michael Adebayo](https://github.com/MichAdebayo) 💻🚀