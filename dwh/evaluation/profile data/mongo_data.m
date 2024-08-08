% Connect to MongoDB and fetch data
% Create a connection to the MongoDB database
conn = mongoc('IP_ADDRESS_GOES_HERE', 27017, 'raw_data');

% Fetch data from the collection
collection = find(conn, 'KGL_LIN_PRF_USA');

% Close database connection
close(conn);

% Now 'profiles' contains your data from MongoDB
% You can start working with this data in MATLAB

% Display the first few rows of the data
head(collection)

% Get information about the table structure
disp(collection)
