# Django Assignment: Placement Statistics API

This Django project provides a RESTful API to fetch placement statistics for students. The API exposes a GET endpoint at `/api/v1/statistics/` that returns statistical insights such as highest CTC, lowest CTC, average CTC, median CTC, percentage of students placed, and a list of students with their placement details.

---

## **Getting Started**

Follow these steps to set up and run the project locally.

### **1. Clone the Repository**

Clone the repository to your local machine:

```bash
git clone https://github.com/suhas-rp/django-cdc.git
cd django-cdc
```

### **2. Create and Activate Virtual Environment**

Create a virtual environment for better dependency management:

```bash
python -m venv venv
source venv/bin/activate    # On Windows use: venv\Scripts\activate
#if execution policy is set to restricted make it unrestricted if you find errors to activate virtual environment
Set-Execution-Policy Unrestricted -scope process
```

### **3. Install Dependencies**

Install the required packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### **4. Database Migration**
go into mysite folder
Run the following commands to apply database migrations:

```bash
cd mysite
python manage.py makemigrations
python manage.py migrate
```

### **5. Load Sample Data**

to load csv data into the sqlite database:

```bash
python manage.py import_data
```

### **6. Run the Development Server**

Start the Django development server:

```bash
python manage.py runserver
```

### **7. Access the API Endpoint**

Once the server is running, you can access the API at:

```
http://localhost:8000/api/statistics/
```

### **8. Example JSON Response**

```json
{
  "highest_ctc": { "CSE": 30.0, "EE": 18.5 },
  "median_ctc": { "CSE": 22.5, "EE": 15.0 },
  "lowest_ctc": { "CSE": 12.0, "EE": 10.5 },
  "average_ctc": { "CSE": 20.6, "EE": 14.7 },
  "percentage_placed": { "CSE": 90.0, "EE": 75.0 },
  "students": [
    {
      "rollno": "210010001",
      "branch": "CSE",
      "batch": "2021",
      "companies_selected": ["Google", "Microsoft"],
      "ctc": 30.0
    },
    {
      "rollno": "210010002",
      "branch": "EE",
      "batch": "2021",
      "companies_selected": ["Texas Instruments"],
      "ctc": 18.5
    }
  ]
}
```

---

Now you're all set to explore the Placement Statistics API! 🚀

