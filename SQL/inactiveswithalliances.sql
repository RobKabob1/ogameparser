--SQL script to find all inactive players, their planets, their alliance info, and only show relevant fields

select 
	players."playerID",
	players."playerName",
	players."playerStatus",
	alliances."allianceName",
	alliances."alliancePlayerCount",
	alliances."allianceTotalScore",
	players."playerTotalScore",
	players."playerEconomyScore",
	players."playerResearchScore",
	players."playerMilitaryHighLevelScore",
	planets."planet1Name",
	planets."planet1Coords",
	planets."planet2Name",
	planets."planet2Coords",
	planets."planet3Name",
	planets."planet3Coords",
	planets."planet4Name",
	planets."planet4Coords",
	planets."planet5Name",
	planets."planet5Coords",
	planets."planet6Name",
	planets."planet6Coords",
	planets."planet7Name",
	planets."planet7Coords",
	planets."planet8Name",
	planets."planet8Coords",
	planets."planet9Name",
	planets."planet9Coords"
FROM players 
INNER JOIN planets ON players."playerID" = planets."playerID"
LEFT JOIN alliances ON players."playerAlliance" = alliances."allianceID"
WHERE players."fetchDate" >= CURRENT_DATE
	AND players."playerStatus" LIKE '%i%'
	AND (alliances."fetchDate" >= CURRENT_DATE OR alliances."fetchDate" IS NULL)
ORDER BY players."playerTotalPosition" ASC