--SQL script to remove all entries into the DB from today

/*
--Delete current day results from players table
DELETE FROM players
WHERE players."fetchDate" >= CURRENT_DATE;

--Delete current day results from alliances table
DELETE FROM alliances
WHERE alliances."fetchDate" >= CURRENT_DATE;

--Delete current day results from planets table
DELETE FROM planets
WHERE planets."fetchDate" >= CURRENT_DATE;
*/