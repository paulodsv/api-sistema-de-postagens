CREATE_POSTINGS = """
INSERT INTO postings (client_id, description, weight_kg, volume_cm3, freight_price, tracking_code)
VALUES ($1, $2, $3, $4, $5, $6)
RETURNING id, client_id, description, freight_price, tracking_code, status, created_at;
"""

SELECT_POSTING_BY_TRACKING_CODE = """
SELECT client_id, description, weight_kg, volume_cm3, freight_price, status, shipped_at, delivered_at
FROM postings 
WHERE tracking_code = $1;
"""

UPDATE_POSTING_STATUS = """
UPDATE postings
SET status = $1 WHERE id = $2
RETURNING id, status;
"""

DELETE_POSTING = """
DELETE FROM postings
WHERE id = $1
RETURNING id;
"""