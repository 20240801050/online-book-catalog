# Online Book Catalog

A cloud-native web application developed using Flask and SQLite to manage a collection of books. The project demonstrates containerization, Kubernetes deployment, CI/CD automation, and GitOps.

## Features

- Add books with title, author, ISBN, genre, and publication year
- View all books in the catalog
- Search books by title, author, or ISBN
- Delete books from the catalog
- Prevent duplicate ISBN entries

## Technology Stack

- Python 3.12
- Flask
- SQLite
- Docker
- Kubernetes (Kind)
- GitHub Actions
- Argo CD

## Run Locally

Clone the repository:

```bash
git clone https://github.com/20240801050/online-book-catalog.git
cd online-book-catalog
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open http://localhost:5000 in your browser.

## Run with Docker

Build the image:

```bash
docker build -t online-book-catalog:1.0 .
```

Run the container:

```bash
docker run -d -p 5000:5000 --name online-book-catalog online-book-catalog:1.0
```

Open http://localhost:5000.

## Kubernetes and GitOps

The application will be deployed using Kubernetes on Kind. Argo CD will monitor the GitHub repository and synchronize Kubernetes manifests automatically.

## Author

Cloud-Native Application Deployment Project