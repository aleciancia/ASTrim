import time
import sqlite3
from typing import List, Dict

class DataPipeline:
    """
    Gestisce l'estrazione, la trasformazione e il caricamento (ETL) dei dati utente.
    Questa è l'interfaccia principale che espone i metodi pubblici per il sistema.
    """

    def __init__(self, db_path: str, max_retries: int = 3) -> None:
        """Inizializza la connessione al database e le impostazioni di retry."""
        self.db_path = db_path
        self.max_retries = max_retries
        self._connection = None
        self._connect()

    def _connect(self) -> None:
        # Molta logica interna di connessione che all'LLM non serve conoscere
        print(f"Connecting to {self.db_path}...")
        self._connection = sqlite3.connect(self.db_path)
        time.sleep(1.5)  # Simula latenza di rete
        print("Connected successfully.")

    def process_user_data(self, raw_data: List[Dict[str, str]]) -> bool:
        """
        Pulisce i dati grezzi degli utenti e li inserisce nel database.
        Restituisce True se l'operazione ha successo per tutti i record, False altrimenti.
        """
        if not raw_data:
            return False
        
        # Simulazione di trasformazioni interne pesanti
        cleaned_data = []
        for record in raw_data:
            name = record.get("name", "").strip().title()
            email = record.get("email", "").strip().lower()
            
            # Validazione superflua per il contesto esterno
            if name and "@" in email and len(email) > 5:
                cleaned_data.append((name, email))
        
        try:
            cursor = self._connection.cursor()
            cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", cleaned_data)
            self._connection.commit()
            return True
        except Exception as e:
            print(f"Database error during insertion: {e}")
            self._connection.rollback()
            return False