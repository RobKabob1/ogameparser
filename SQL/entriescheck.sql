--SQL script group entries by counts to make sure entries are working successfully

select "fetchDate", Count("fetchDate") from "alliances"
Group by "fetchDate"
ORDER by "fetchDate" DESC;