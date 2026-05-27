SELECT * from bronze.train_metadata
WHERE train_no = ?
and success = True
and created_at::DATE = CURRENT_DATE
