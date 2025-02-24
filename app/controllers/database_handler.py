import psycopg2
from psycopg2.extras import RealDictCursor
from models.user import User

class DatabaseHandler:
    def __init__(self, db_url):
        """
        Initialise le DatabaseHandler avec l'URL de la base de données.
        """
        self.db_url = db_url

    def connect(self):
        """
        Retourne une connexion à la base de données PostgreSQL.
        """
        return psycopg2.connect(self.db_url)
    
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
        cursor = conn.cursor()

        # Exemple de création de table pour les utilisateurs
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
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO users (email, password)
            VALUES (%s, %s)
            RETURNING id
        ''', (user.email, user.password))

        user.id = cursor.fetchone()[0]  # Récupère l'ID généré
        conn.commit()
        conn.close()

    def get_user_by_email(self, email):
        """
        Récupère un utilisateur par son email.
        """
        conn = self._get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute('''
            SELECT * FROM users WHERE email = %s
        ''', (email,))

        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            # Retourne un objet User avec les données récupérées
            return User(id=user_data['id'], email=user_data['email'], password=user_data['password'])
        return None

    def update_user(self, user):
        """
        Met à jour un utilisateur dans la base de données.
        """
        conn = self._get_connection()
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
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM users WHERE id = %s
        ''', (user_id,))

        conn.commit()
        conn.close()