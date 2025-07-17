import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from app.core.config import settings
import psycopg2

def test_connection():
    print("Testing direct psycopg2 connection...")
    print(f"Connection URL: {settings.POSTGRES_URL}")
    
    # Extract connection parameters from URL
    url = settings.POSTGRES_URL
    if url.startswith('postgresql+psycopg2://'):
        url = url.replace('postgresql+psycopg2://', '')
    elif url.startswith('postgresql://'):
        url = url.replace('postgresql://', '')
    
    # Parse the URL
    if '@' in url:
        auth, rest = url.split('@', 1)
        if ':' in auth:
            username, password = auth.split(':', 1)
        else:
            username = auth
            password = ''
        
        if ':' in rest:
            host_port, database = rest.split('/', 1)
            if ':' in host_port:
                host, port = host_port.split(':', 1)
                port = int(port)
            else:
                host = host_port
                port = 5432
        else:
            host = rest
            port = 5432
            database = ''
    else:
        print("Invalid connection string format")
        return
    
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Database: {database}")
    print(f"Username: {username}")
    print(f"Password: {'*' * len(password) if password else 'None'}")
    
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password,
            options="-c client_encoding=utf8"
        )
        print("✅ Connection successful!")
        conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    test_connection() 