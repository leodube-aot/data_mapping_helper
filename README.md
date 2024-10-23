# Data mapping helper

Creates a db table mapping for a specific filing type code.

### Description

This script works by:
1. Finding a list of FILING entries by FILING_TYP_CD. This list is limited using the MAX_FILINGS variable. For these results we only care about the EVENT_IDS.
2. We use these event ids to create sort of a "root" node to build the mapping around. The EVENT table has many foreign keys referencing it from other tables (these can be thought of as child tables).
3. We populate the event child tables list by getting all referencing constraints.
4. For the child tables, we can then recursively populate their child tables, up to the MAX_MAPPING_DEPTH

Notes:
- The SQL query I use on step 4 isn't perfect. It makes the assumption that the fk column name and pk column name are the same. You'll see log entries that say certain columns cannot be found for a specific. For now, you can just check whether any of these tables might contain useful migration data manually.
```
// Example debug log entries:

// This one happens since CORP_NAME has START_EVENT_ID and END_EVENT_ID, but not EVENT_ID. 
// The EVENT_ID debug logs aren't really an issue since it refers back to the root event table.
Could not find column EVENT_ID in table CORP_NAME.

// This means that PARTY_TYP_CD refers to another table, but none of the entries relating to
// the filing type have a value (ie. only null values), so we can ignore this fk.
Only NULL values for PARTY_TYP_CD in table FILING_USER.
```

### Usage

1. Create a new `.env` file from the sample file. Enter the `COLIN DEV` readonly connection details.
2. Run `make setup`
3. Update the config variables in `data_mapping_helper.py` and `models.py` as necessary. I haven't had a chance to move these into a dedicated config file, but I include a brief description below:
- `data_mapping_helper.FILING_TYP_CD`: The specific colin filing type you want to create the mapping for.
- `data_mapping_helper.MAX_FILINGS`: The maximum number of filings to use to create the mapping.
- `models.VERBOSE`: If True, will print the rows associated with each child table mapping. Can be useful for debugging, or further digging.
- `models.MAX_MAPPING_DEPTH`: The mapping recursion depth level. I find that 2 is mostly ideal. Any more and you start getting recursive loops. The reason you might want to increase this is that some tables rely on other tables, and capturing this in the mapping output might be beneficial.


### Screenshots
<img src="screenshots/Screenshot%201.png" alt="drawing" width="600"/>

---

<img src="screenshots/Screenshot%202.png" alt="drawing" width="900"/>

---

<img src="screenshots/Screenshot%203.png" alt="drawing" width="600"/>
