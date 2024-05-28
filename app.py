import os
import time
import base64
import psycopg2
from psycopg2 import pool
from flask import Flask, request, render_template, redirect, url_for
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask app configuration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# OpenAI client setup
client = OpenAI(organization=os.environ['OPENAI_ORG_ID'])

# Database connection pool setup
try:
    conn_pool = psycopg2.pool.SimpleConnectionPool(
        1, 20,
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        host=os.environ['DB_HOST'],
        port="5432",
        database=os.environ['DB_NAME']
    )
except Exception as error:
    print(f"Error creating connection pool: {error}")

def get_db_connection():
    if conn_pool:
        return conn_pool.getconn()
    else:
        raise ConnectionError("Connection pool is not initialized")

def release_db_connection(conn):
    if conn_pool:
        conn_pool.putconn(conn)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_chart(chart_path):
    base64_image = encode_image(chart_path)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this chart. Include the symbol and discuss the price action."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ]
    )
    return response.choices[0].message.content

def store_analysis_in_db(user_id, chart_filename, analysis):
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        cur.execute(
            """
            INSERT INTO chart_analysis (user_id, chart_path, analysis_text, timestamp)
            VALUES (%s, %s, %s, %s)
            """, (user_id, chart_filename, analysis, timestamp)
        )
        conn.commit()
    except Exception as error:
        print(f"Error storing analysis in database: {error}")
    finally:
        if cur:
            cur.close()
        if conn:
            release_db_connection(conn)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        try:
            analysis = analyze_chart(filepath)
            user_id = 1  # Example user ID, replace with dynamic user authentication
            store_analysis_in_db(user_id, filepath, analysis)
            return render_template('result.html', analysis=analysis)
        except Exception as error:
            print(f"Error processing file: {error}")
            return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
