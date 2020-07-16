#! /usr/bin/env python3

import psycopg2

question1 = "1. What are the most popular three articles of all time?"

query1 = ("""
SELECT a.title,count(*) AS num
FROM articles a, log l
WHERE a.slug = substring(l.path, 10)
GROUP BY a.title
ORDER BY num DESC
LIMIT 3;
""")

question2 = "2. Who are the most popular article authors of all time?"

query2 = ("""
SELECT au.name,count(*) AS num
FROM articles ar, authors au, log l
WHERE ar.author = au.id and ar.slug = substring(l.path, 10)
and l.status like '200%'
GROUP BY au.name
ORDER BY num DESC
LIMIT 3;
""")

question3 = "3. On which days did more than 1% of requests lead to errors?"

query3 = ("""
SELECT AllReq.logDate,
round(((100.0*FailReq.ReqCount)/(AllReq.ReqCount)),3) AS errors
FROM
    (SELECT to_char(TIME,'Mon DD, YYYY') AS logDate,count(*) AS ReqCount
     FROM log
     GROUP BY to_char(TIME,'Mon DD, YYYY')) AS AllReq,
    (SELECT to_char(TIME,'Mon DD, YYYY') AS logDate,count(*) AS ReqCount
     FROM log
     WHERE (status like '4%' or status like '5%')
     GROUP BY to_char(TIME, 'Mon DD, YYYY')) AS FailReq
     WHERE AllReq.logDate=FailReq.logDate
     AND ((100.0*FailReq.ReqCount)/(AllReq.ReqCount)) > 1;
""")


# Connect to the db and feed query to extract


def get_queryResults(sql_query):
    try:
        db = psycopg2.connect(database="news")
        c = db.cursor()
        c.execute(sql_query)
        results = c.fetchall()
        db.close()
    except ValueError:
        print("Oops!, There is an error")
    return results


result1 = get_queryResults(query1)
result2 = get_queryResults(query2)
result3 = get_queryResults(query3)


# print functions for query results

def print_res1or2(resultData):
    for key, value in resultData:
        print("\t{} - {} views".format(key, value))
    print("\n")


def print_res3(resultData):
    for key, value in resultData:
        print("\t{} - {}% views".format(key, value))
    print("\n")


# print results


print(question1)
print_res1or2(result1)
print(question2)
print_res1or2(result2)
print(question3)
print_res3(result3)
