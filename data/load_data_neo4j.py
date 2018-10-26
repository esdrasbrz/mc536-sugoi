from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver(
    "bolt://localhost:7687", 
    auth=basic_auth("neo4j", "sugoi"))
session = driver.session()

create_queries = [
    '''
    MATCH ()-[s:SIMILAR_TO]-()
    DELETE s
    ''',
    '''
    MATCH ()-[c:CAUSES]-()
    DELETE c
    ''',
    '''
    MATCH (n)
    DELETE n
    ''',
    '''
    LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/esdrasbrz/mc536-sugoi/master/data/ncomms-disease.csv" AS line
    FIELDTERMINATOR '|'
    CREATE (d:Disease {name: line.name, occurrences: toInt(line.occurrences)})
    ''',
    '''
    LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/esdrasbrz/mc536-sugoi/master/data/ncomms-symptom.csv" AS line
    FIELDTERMINATOR '|'
    CREATE (s:Symptom {name: line.name, occurrences: toInt(line.occurrences)})
    ''',
    '''
    LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/esdrasbrz/mc536-sugoi/master/data/ncomms-cause.csv" AS line
    FIELDTERMINATOR '|'
    MATCH (s:Symptom {name: line.symptom})
    MATCH (d:Disease {name: line.disease})
    CREATE (d)-[:CAUSES {occurrences: line.occurrences, score: toFloat(line.score)}]->(s)
    ''',
    '''
    LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/esdrasbrz/mc536-sugoi/master/data/ncomms-similarity.csv" AS line
    FIELDTERMINATOR '|'
    MATCH (f:Disease {name: line.disease_from})
    MATCH (t:Disease {name: line.disease_to})
    CREATE (f)-[:SIMILAR_TO {score: toFloat(line.score)}]->(t)
    '''
]

for q in create_queries:
    print(q)
    session.run(q)
    print('done!\n')
