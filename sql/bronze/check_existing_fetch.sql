SELECT * from bronze.train_metadata
WHERE train_no = ?
and success = True
and run_date::DATE = ?
