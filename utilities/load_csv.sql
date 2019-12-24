LOAD CSV FROM 'file:///country.csv' AS line CREATE (:Country { country_id: line[0], country_name: line[1]})
LOAD CSV FROM 'file:///war.csv' AS line CREATE (:War { war_id: line[0], war_name: line[1],death_number:line[2] })
LOAD CSV FROM 'file:///year.csv' AS line CREATE (:Year { year_id: line[0], date: line[1]})
LOAD CSV FROM 'file:///location.csv' AS line CREATE (:Location { location_id: line[0], location_name: line[1]})
LOAD CSV FROM 'file:///win.csv' AS line MATCH (a:Country), (m:War) WHERE a.country_id = line[1] AND m.war_id = line[2] CREATE (a) - [r:WIN] -> (m) RETURN r
LOAD CSV FROM 'file:///defeated.csv' AS line MATCH (a:War), (m:Country) WHERE a.war_id = line[2] AND m.country_id = line[1] CREATE (a) - [r:DEFEATED] -> (m) RETURN r
LOAD CSV FROM 'file:///start.csv' AS line MATCH (a:War), (m:Year) WHERE a.war_id = line[1] AND m.year_id = line[2] CREATE (a) - [r:START] -> (m) RETURN r
LOAD CSV FROM 'file:///end.csv' AS line MATCH (a:Year), (m:War) WHERE a.year_id = line[2] AND m.war_id = line[1] CREATE (a) - [r:END] -> (m) RETURN r
LOAD CSV FROM 'file:///where_to_combat.csv' AS line MATCH (a:War), (m:Location) WHERE a.war_id = line[1] AND m.location_id = line[2] CREATE (a) - [r:LOCATED] -> (m) RETURN r
