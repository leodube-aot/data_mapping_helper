"""Get tables with non-null foreign keys for a given COLIN filing event"""

import os
import cx_Oracle

from dotenv import find_dotenv, load_dotenv

from models import EventTable


# Load all the envars from a .env file located in the project root
load_dotenv(find_dotenv())


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# UPDATE MAPPING VARIABLES HERE
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
FILING_TYP_CD = "NOALC"
MAX_FILINGS = 100


# Setup Oracle
dsn = f"{os.getenv('ORACLE_HOST')}:{os.getenv('ORACLE_PORT')}/{os.getenv('ORACLE_DB_NAME')}"
cx_Oracle.init_oracle_client(
    lib_dir=os.getenv("ORACLE_INSTANT_CLIENT_DIR")
)  # this line may not be required for some
connection = cx_Oracle.connect(
    user=os.getenv("ORACLE_USER"), password=os.getenv("ORACLE_PASSWORD"), dsn=dsn
)
cursor = connection.cursor()


# Check connection
cursor.execute(
    "SELECT filing_typ_cd, full_desc FROM filing_type WHERE filing_typ_cd=:filing_typ_cd",
    filing_typ_cd=FILING_TYP_CD,
)
filing_typ_cd, full_desc = cursor.fetchone()


# Get filings with filing type code
cursor.execute(
    "SELECT event_id FROM filing WHERE filing_typ_cd=:filing_typ_cd FETCH FIRST :limit ROWS ONLY",
    filing_typ_cd=filing_typ_cd,
    limit=MAX_FILINGS,
)
filing_event_ids = [event_id[0] for event_id in cursor.fetchall()]


# Get foreign keys for EVENT table
events = EventTable(filing_type_code=filing_typ_cd, event_ids=filing_event_ids)
events.build_mapping(cursor)

print(f"\n\nTable mapping for {filing_typ_cd}: {full_desc}", end="\n\n")
events.print()

# Close cursor
cursor.close()
