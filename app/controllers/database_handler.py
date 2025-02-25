import psycopg2
from psycopg2.extras import RealDictCursor
from models.user import User

DATABASE_URL = "postgresql://postgres:postgres@db:5432/postgres"


class DatabaseHandler:
    def __init__(self, DATABASE_URL):
        """
        Initialise le DatabaseHandler avec l'URL de la base de données.
        """
        self.db_url = DATABASE_URL

    def connect(self):
        """
        Retourne une connexion à la base de données PostgreSQL.
        """
        try:
            conn = psycopg2.connect(self.db_url)
            print("Database connection successful!")
            return conn
        except psycopg2.Error as e:
            print(f"Database connection failed: {e}")
            return None

    def disconnect(self):
        """
        Close any existing connections
        Should switch self.is_connected.
        """

    def create_tables(self):
        """
        Crée les tables nécessaires dans la base de données.
        """
        conn = self.connect()
        if conn is None:
            print("Failed to connect to the database. Tables not created.")
            return

        cursor = conn.cursor()

        # Création de la table des utilisateurs
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        ''')

        conn.commit()
        conn.close()

    def save_user(self, user):
        """
        Sauvegarde un utilisateur dans la base de données.
        """
        conn = self.connect()
        if conn is None:
            print("Failed to connect to the database. Cannot save user.")
            return None  

        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (email, password)
            VALUES (%s, %s)
            RETURNING id
        ''', (user.email, user.password))

        user_id = cursor.fetchone()
        if user_id:
            user.id = user_id[0]  # ✅ Stocke l'ID dans l'objet user
        
        conn.commit()
        conn.close()

        print(f"User ID after saving: {user.id}")  # ✅ Doit afficher un ID valide


    def get_user_by_email(self, email):
        """
        Récupère un utilisateur par son email.
        """
        conn = self.connect()
        if conn is None:
            print("Failed to connect to the database. Cannot fetch user.")
            return None

        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''
            SELECT * FROM users WHERE email = %s
        ''', (email,))
        
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            return User(id=user_data['id'], email=user_data['email'], password=user_data['password'])
        return None

    def update_user(self, user):
        """
        Met à jour un utilisateur dans la base de données.
        """
        conn = self.connect()
        if conn is None:
            print("Failed to connect to the database. Cannot update user.")
            return None
        
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users
            SET email = %s, password = %s
            WHERE id = %s
        ''', (user.email, user.password, user.id))

        conn.commit()
        conn.close()

    def delete_user(self, user_id):
        """
        Supprime un utilisateur de la base de données.
        """
        conn = self.connect()
        if conn is None:
            print("Failed to connect to the database. Cannot delete user.")
            return None
        
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM users WHERE id = %s
        ''', (user_id,))

        conn.commit()
        conn.close()
