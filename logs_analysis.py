#! /usr/bin/env python3

import psycopg2

question1 = "1. What are the most popular three articles of all time? Which articles have been accessed the most?"

query1 = (""" 
			SELECT a.title, count(*) AS num
			FROM articles a, log l 
			WHERE a.slug = substring(l.path, 10)
			GROUP BY a.title
			ORDER BY num DESC
			LIMIT 3;
			""")

question2 = "2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views?"

query2 = (""" 
			SELECT au.name, count(*) AS num 
			FROM articles ar, authors au, log l
			WHERE ar.author = au.id and ar.slug = substring(l.path, 10) and l.status LIKE '%200%OK%'
			GROUP BY au.name
			ORDER BY num DESC
			LIMIT 3; 
			""")

question3 = "3. On which days did more than 1% of requests lead to errors?"

query3 = ("""
            SELECT AllReq.log_date, round((100.0*FailReq.ReqCount)/(AllReq.ReqCount)) AS errors
            FROM
               (SELECT to_char(TIME, 'Mon DD, YYYY') AS log_date, count(*) AS ReqCount
                FROM log
                GROUP BY to_char(TIME, 'Mon DD, YYYY')) AS AllReq,
               (SELECT to_char(TIME, 'Mon DD, YYYY') AS log_date, count(*) AS ReqCount
                FROM log
                WHERE (status like '4%' or status like '5%') -- client or network error 
                GROUP BY to_char(TIME, 'Mon DD, YYYY')) AS FailReq
             WHERE AllReq.log_date=FailReq.log_date
               AND ((100*FailReq.ReqCount)/(AllReq.ReqCount)) > 1;
               """)


# Connect to the db and feed query to extract


def get_queryResults(sql_query):
    db = psycopg2.connect(database="news")
    c = db.cursor()
    c.execute(sql_query)
    results = c.fetchall()
    db.close()
    return results


result1 = get_queryResults(query1)
result2 = get_queryResults(query2)
result3 = get_queryResults(query3)


# print functions for query results

def print_res1or2(resultData):
    for indx in range(len(resultData)):
        title = resultData[indx][0]
        res = resultData[indx][1]
        print("\t" + "%s - %d" % (title, res) + " views")
    print("\n")


def print_res3(resultData):
    for indx in range(len(resultData)):
        title = resultData[indx][0]
        res = resultData[indx][1]
        print("\t" + "%s - %d" % (title, res) + "% views")
    print("\n")

# print results

print(question1)
print_res1or2(result1)
print(question2)
print_res1or2(result2)
print(question3)
print_res3(result3)
