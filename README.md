# Qazan AI 📊🤖

This repository hosts the Minimum Viable Product (MVP) of Qazan AI's future technical analysis tool. Our SaaS platform aims to provide investors with AI-enhanced insights, giving them a competitive edge in financial markets.

## 🚀**Project Overview**
Qazan AI leverages cutting-edge artificial intelligence to analyze financial charts and offer actionable insights for investors. This MVP demonstrates our core functionality through a user-friendly web interface built with Flask and served by Nginx. Users can upload graphs of financial asset quotations and receive detailed AI-generated analyses to inform their investment decisions.

##✨**Features**
Upload Financial Charts: Users can upload images of financial asset charts directly through the web interface.
AI-Driven Analysis: The application utilizes OpenAI's GPT-4 to analyze uploaded charts and generate investment insights.
Secure and Scalable Backend: Powered by Flask for the web server and PostgreSQL for database management.
User-Friendly Interface: Intuitive web design for seamless user experience.
Tech Stack
Frontend: HTML, CSS, JavaScript
Backend: Python, Flask
AI Engine: OpenAI GPT-4
Database: PostgreSQL
Server: Nginx
Environment Management: Python-dotenv

##🛠️**Getting Started**
Follow these instructions to set up and run the project locally.

##🏁**Prerequisites**
Python 3.8 or higher
PostgreSQL
Nginx
Pipenv (optional but recommended for environment management)


##Installation

###Clone the Repository
```
git clone https://github.com/yourusername/qazan.git
cd qazan
```

###Install Dependencies
```
pip install -r requirements.txt
```

###Set Up Environment Variables
Create a .env file in the root directory and add your environment variables:
```
OPENAI_ORG_ID=your_openai_org_id
OPENAI_API_KEY=your_openai_api_key
DB_USER=your_db_user
DB_PASS=your_db_password
DB_HOST=your_db_host
DB_NAME=your_db_name
```

###Database Migration
```
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

###Run the Application
```
flask run
```

###Nginx Configuration
To serve the Flask app through Nginx, configure your Nginx server block as follows:
```
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path_to_your_project/static;
    }
}
```

##🌐 Usage
**Access the Web Interface**
Open your browser and navigate to http://your_domain.com.

##📈**Upload a Chart**
Click the upload button and select a financial asset chart image (PNG, JPG, or JPEG).

##**Receive Analysis**
The AI will analyze the uploaded chart and provide investment insights on the results page.

##🤝 **Contributing**
We welcome contributions from the community. To contribute:

Fork the repository.
Create a feature branch.
Commit your changes.
Push to your branch.
Create a pull request.
Please adhere to the project's Code of Conduct and see CONTRIBUTING.md for detailed guidelines.

##📄**License**

##📬**Contact**
For any inquiries or feedback, please contact us at nima@vigilantia.fr

Thank you for being part of Qazan AI's journey to revolutionize financial market analysis with AI!

By Vigilantia - Proudly from Metz

Feel free to customize further as per your project's needs!
