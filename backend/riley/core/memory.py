import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

class MemoryEngine:
    def __init__(self):
        """
        Initialize the memory engine with a database connection
        """
        self.db_url = os.getenv('DATABASE_URL')
        
    def _get_connection(self):
        """
        Get a database connection
        """
        return psycopg2.connect(self.db_url)
    
    def store_interaction(self, user_id, query, response, intent=None, mode=None, emotion_detected=None, emotion_response=None):
        """
        Store a user interaction in the database
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO riley.interactions 
                    (user_id, query, response, intent, mode, emotion_detected, emotion_response) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (user_id, query, response, intent, mode, emotion_detected, emotion_response)
                )
                interaction_id = cursor.fetchone()[0]
                return interaction_id
    
    def store_memory(self, user_id, memory_type, key, value):
        """
        Store a memory item in the database
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                # Convert value to JSON if it's a dict or list
                if isinstance(value, (dict, list)):
                    value_json = json.dumps(value)
                else:
                    value_json = json.dumps({"value": value})
                
                # Check if memory already exists
                cursor.execute(
                    "SELECT id FROM riley.memory WHERE user_id = %s AND type = %s AND key = %s",
                    (user_id, memory_type, key)
                )
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing memory
                    cursor.execute(
                        """
                        UPDATE riley.memory 
                        SET value = %s, timestamp = NOW() 
                        WHERE user_id = %s AND type = %s AND key = %s
                        RETURNING id
                        """,
                        (value_json, user_id, memory_type, key)
                    )
                else:
                    # Insert new memory
                    cursor.execute(
                        """
                        INSERT INTO riley.memory 
                        (user_id, type, key, value) 
                        VALUES (%s, %s, %s, %s)
                        RETURNING id
                        """,
                        (user_id, memory_type, key, value_json)
                    )
                
                memory_id = cursor.fetchone()[0]
                return memory_id
    
    def retrieve_memory(self, user_id, memory_type='all', limit=10):
        """
        Retrieve memory items from the database
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                if memory_type == 'all':
                    cursor.execute(
                        """
                        SELECT * FROM riley.memory 
                        WHERE user_id = %s 
                        ORDER BY timestamp DESC 
                        LIMIT %s
                        """,
                        (user_id, limit)
                    )
                else:
                    cursor.execute(
                        """
                        SELECT * FROM riley.memory 
                        WHERE user_id = %s AND type = %s 
                        ORDER BY timestamp DESC 
                        LIMIT %s
                        """,
                        (user_id, memory_type, limit)
                    )
                
                results = cursor.fetchall()
                
                # Parse JSON values
                for result in results:
                    try:
                        result['value'] = json.loads(result['value'])
                    except:
                        pass
                
                return results
    
    def store_fact(self, user_id, fact, source=None, confidence=1.0):
        """
        Store a fact in the database
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO riley.facts 
                    (user_id, fact, source, confidence) 
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (user_id, fact, source, confidence)
                )
                fact_id = cursor.fetchone()[0]
                return fact_id
    
    def retrieve_facts(self, user_id, source=None, limit=10):
        """
        Retrieve facts from the database
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                if source:
                    cursor.execute(
                        """
                        SELECT * FROM riley.facts 
                        WHERE user_id = %s AND source = %s 
                        ORDER BY timestamp DESC 
                        LIMIT %s
                        """,
                        (user_id, source, limit)
                    )
                else:
                    cursor.execute(
                        """
                        SELECT * FROM riley.facts 
                        WHERE user_id = %s 
                        ORDER BY timestamp DESC 
                        LIMIT %s
                        """,
                        (user_id, limit)
                    )
                
                return cursor.fetchall()
    
    def get_user_settings(self, user_id):
        """
        Get user settings from the database
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM riley.user_settings WHERE user_id = %s",
                    (user_id,)
                )
                
                settings = cursor.fetchone()
                
                if not settings:
                    # Create default settings
                    cursor.execute(
                        """
                        INSERT INTO riley.user_settings 
                        (user_id, default_mode, voice_enabled, allow_self_editing, allowed_tools) 
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING *
                        """,
                        (user_id, 'assistant', True, False, json.dumps(["invention", "web_search", "wiki"]))
                    )
                    settings = cursor.fetchone()
                
                # Parse JSON values
                if settings and 'allowed_tools' in settings:
                    try:
                        settings['allowed_tools'] = json.loads(settings['allowed_tools'])
                    except:
                        pass
                
                return settings
    
    def update_user_settings(self, user_id, settings):
        """
        Update user settings in the database
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Check if settings exist
                cursor.execute(
                    "SELECT * FROM riley.user_settings WHERE user_id = %s",
                    (user_id,)
                )
                
                existing = cursor.fetchone()
                
                # Prepare allowed_tools as JSON
                if 'allowed_tools' in settings and not isinstance(settings['allowed_tools'], str):
                    settings['allowed_tools'] = json.dumps(settings['allowed_tools'])
                
                if existing:
                    # Update fields that are provided
                    update_fields = []
                    update_values = []
                    
                    for key, value in settings.items():
                        if key != 'user_id':
                            update_fields.append(f"{key} = %s")
                            update_values.append(value)
                    
                    update_values.append(user_id)
                    update_values.append(datetime.now())
                    
                    cursor.execute(
                        f"""
                        UPDATE riley.user_settings 
                        SET {', '.join(update_fields)}, updated_at = %s 
                        WHERE user_id = %s
                        RETURNING *
                        """,
                        update_values + [user_id]
                    )
                else:
                    # Insert new settings
                    fields = ['user_id']
                    values = [user_id]
                    placeholders = ['%s']
                    
                    for key, value in settings.items():
                        if key != 'user_id':
                            fields.append(key)
                            values.append(value)
                            placeholders.append('%s')
                    
                    cursor.execute(
                        f"""
                        INSERT INTO riley.user_settings 
                        ({', '.join(fields)}) 
                        VALUES ({', '.join(placeholders)})
                        RETURNING *
                        """,
                        values
                    )
                
                updated_settings = cursor.fetchone()
                
                # Parse JSON values
                if updated_settings and 'allowed_tools' in updated_settings:
                    try:
                        updated_settings['allowed_tools'] = json.loads(updated_settings['allowed_tools'])
                    except:
                        pass
                
                return updated_settings
    
    def store_invention(self, user_id, prompt, invention):
        """
        Store an invention in the database
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO riley.inventions 
                    (user_id, prompt, invention) 
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (user_id, prompt, json.dumps(invention))
                )
                invention_id = cursor.fetchone()[0]
                return invention_id
    
    def store_search(self, user_id, query, results):
        """
        Store search results in the database
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO riley.search_history 
                    (user_id, query, results) 
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (user_id, query, json.dumps(results))
                )
                search_id = cursor.fetchone()[0]
                return search_id
    
    def store_github_analysis(self, user_id, repo_url, analysis):
        """
        Store GitHub repository analysis in the database
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO riley.github_analysis 
                    (user_id, repo_url, analysis) 
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (user_id, repo_url, json.dumps(analysis))
                )
                analysis_id = cursor.fetchone()[0]
                return analysis_id
    
    def store_code_repair(self, user_id, original_code, repaired_code, changes):
        """
        Store code repair in the database
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO riley.code_repairs 
                    (user_id, original_code, repaired_code, changes) 
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (user_id, original_code, repaired_code, json.dumps(changes))
                )
                repair_id = cursor.fetchone()[0]
                return repair_id
