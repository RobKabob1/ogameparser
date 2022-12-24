--SQL script to find the size of the database. 
--Supabase allows for 1GB database sizes for the free tier

select pg_database_size('postgres');