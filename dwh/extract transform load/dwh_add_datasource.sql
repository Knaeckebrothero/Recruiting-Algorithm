# This script adds a new datasource to the DWH.DIM_Origin table.
INSERT INTO DWH.DIM_Origin
(abbreviation, mongoCollectionName, name, url, importDate, comment)
VALUES
('PRF', 'KGL_LIN_PRF_USA', 'LinkedIn Profiles', 'https://www.this-is-where-we-got-them.com', NOW(),
 'Kaggle dataset with LinkedIn profiles from the US.');

# To verify the data was added correctly, you can run the following query:
# SELECT * FROM DWH.DIM_Origin;

# Don't forget to commit the transaction!
# COMMIT;
