--SQL script to remove all entries into the DB from today

/*Delete from players table
DELETE from players
WHERE players."fetchDate" >= CURRENT_DATE
*/

/*Delete from alliances table
DELETE from alliances
WHERE alliances."fetchDate" >= CURRENT_DATE
*/

/*
DELETE from planets
*/