import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres.egnmntyafgtdjwdhmtbz:Tz8a4oIdPcPArvuO@aws-0-sa-east-1.pooler.supabase.com:6543/postgres'
SQLALCHEMY_TRACK_MODIFICATIONS = False
