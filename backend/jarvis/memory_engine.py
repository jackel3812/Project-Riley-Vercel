import os
import sqlite3
import json
from datetime import datetime

class MemoryEngine:
    def __init__(self, db_path=None):
        """
        Initialize the memory engine with a database connection
        """
        # Use provided DB path or default to environment variable or SQLite
        self.db_path = db_path or os.getenv('DATABASE_URL', 'riley_memory.db')
        self.is_sqlite = 'sqlite' in self.db_path
        
        # Initialize database
        self._init_db()
    
    def _init_db(self):
        """
        Initialize the database with required tables
        """
        if self.is_sqlite:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create interactions table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                query TEXT,
                intent TEXT,
                response TEXT
            )
            ''')
            
            # Create memory table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                type TEXT,
                key TEXT,
                value TEXT
            )
            ''')
            
            # Create facts table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                fact TEXT,
                source TEXT,
                confidence REAL
            )
            ''')
            
            conn.commit()
            conn.close()
        else:
            # For PostgreSQL or other databases, connection would be handled differently
            # This is a placeholder for future implementation
            pass
    
    def store_interaction(self, query, intent, response=None):
        """
        Store a user interaction in the database
        """
        timestamp = datetime.now().isoformat()
        
        if self.is_sqlite:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT INTO interactions (timestamp, query, intent, response) VALUES (?, ?, ?, ?)',
                (timestamp, query, intent, response)
            )
            
            conn.commit()
            conn.close()
        else:
            # PostgreSQL implementation would go here
            pass
    
    def store_memory(self, memory_type, key, value):
        """
        Store a memory item in the database
        """
        timestamp = datetime.now().isoformat()
        
        if self.is_sqlite:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Convert value to JSON if it's a dict or list
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            
            cursor.execute(
                'INSERT INTO memory (timestamp, type, key, value) VALUES (?, ?, ?, ?)',
                (timestamp, memory_type, key, value)
            )
            
            conn.commit()
            conn.close()
        else:
            # PostgreSQL implementation would go here
            pass
    
    def store_fact(self, fact, source, confidence=1.0):
        """
        Store a fact in the database
        """
        timestamp = datetime.now().isoformat()
        
        if self.is_sqlite:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT INTO facts (timestamp, fact, source, confidence) VALUES (?, ?, ?, ?)',
                (timestamp, fact, source, confidence)
            )
            
            conn.commit()
            conn.close()
        else:
            # PostgreSQL implementation would go here
            pass
    
    def retrieve_memory(self, memory_type, key=None, limit=10):
        """
        Retrieve memory items from the database
        """
        if self.is_sqlite:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if key:
                cursor.execute(
                    'SELECT * FROM memory WHERE type = ? AND key = ? ORDER BY timestamp DESC LIMIT ?',
                    (memory_type, key, limit)
                )
            else:
                cursor.execute(
                    'SELECT * FROM memory WHERE type = ? ORDER BY timestamp DESC LIMIT ?',
                    (memory_type, limit)
                )
            
            results = [dict(row) for row in cursor.fetchall()]
            
            # Parse JSON values
            for result in results:
                try:
                    result['value'] = json.loads(result['value'])
                except:
                    pass
            
            conn.close()
            return results
        else:
            # PostgreSQL implementation would go here
            return []
    
    def retrieve_facts(self, source=None, limit=10):
        """
        Retrieve facts from the database
        """
        if self.is_sqlite:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if source:
                cursor.execute(
                    'SELECT * FROM facts WHERE source = ? ORDER BY timestamp DESC LIMIT ?',
                    (source, limit)
                )
            else:
                cursor.execute(
                    'SELECT * FROM facts ORDER BY timestamp DESC LIMIT ?',
                    (limit,)
                )
            
            results = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return results
        else:
            # PostgreSQL implementation would go here
            return []
    
    def store_search(self, query, results):
        """
        Store search results in memory
        """
        self.store_memory('search', query, results)
    
    def store_calculation(self, equation, solution):
        """
        Store calculation results in memory
        """
        self.store_memory('calculation', equation, solution)
    
    def store_creation(self, creation_type, prompt, result):
        """
        Store creative outputs in memory
        """
        self.store_memory('creation', f"{creation_type}:{prompt}", result)
    
    def store_learning(self, source, identifier, knowledge):
        """
        Store learned information in memory
        """
        self.store_memory('learning', f"{source}:{identifier}", knowledge)
