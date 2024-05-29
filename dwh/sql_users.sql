# Create users 
CREATE USER 'bi_admin'@'%' IDENTIFIED BY 'PASSWORD_GOES_HERE';
CREATE USER 'bi_user'@'%' IDENTIFIED BY 'PASSWORD_GOES_HERE';

# Assign permissions to users
GRANT SELECT ON *.* TO 'bi_admin'@'%'; # Admin can read all
GRANT CREATE ON *.* TO 'bi_admin'@'%'; # Admin has all permissions on his own schemas
# GRANT ALL PRIVILEGES ON *.* TO 'bi_admin'@'localhost';
GRANT SELECT ON DWH.* TO 'bi_user'@'%'; # User can read dwh

# Apply changes
FLUSH PRIVILEGES;
