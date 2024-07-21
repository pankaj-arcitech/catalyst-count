# Tasks

## Follow the installation steps

1. Clone the repository:

```bash
git clone https://github.com/pankajsajekar/catalyst-count.git
```

## A. Setup Project
1. change dir
```
cd catalyst-count
```

2. Create a virtual environment
```
python -m venv venv

```
3. Activate virtual environment
```
command - .\venv\Scripts\activate
```
4. Install packages from requirements file
```
pip install -r requirements.txt
```

6. Create Database 
```
python manage.py makemigrations
python manage.py migrate
```
7. Run server
```
python manage.py runserver
```

8. Createsuper user
```
python manage.py createsuperuser
```
9. If Your Are using My SQLite Database
Login in Djano admin panel using bellow Crediential.
```
Username: admin
Password: 123
```

### Basic Detials

1. Django All-auth interegration Done
2. Query Data set Retrive from DB Done
3. User CRUD functionality Done
4. Upload CSV File data Done but I am trying to show in progress bar