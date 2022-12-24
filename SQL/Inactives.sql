--SQL script find all inactive players and their planets

select * from players
WHERE players."fetchDate" >= CURRENT_DATE
AND players."playerStatus" LIKE '%i%'
ORDER BY players."playerTotalPosition" ASC