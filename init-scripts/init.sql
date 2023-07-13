
-- Connect to sparkdb
\c sparkdb;

-- Create user_data table
CREATE TABLE user_data (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100)
);
