import psycopg2
import streamlit as st
import sqlparse
from sql_metadata.parser import Parser #gives a quick way to get the tables, columns, and aliases from an SQL query. not perfect

'''default query 
SELECT count(*) from ((SELECT a.id, a.fname, a.lname FROM actor a) 
EXCEPT (SELECT DISTINCT ac.id, ac.fname, ac.lname FROM actor_casts ac 
JOIN genre g ON ac.mid = g.mid JOIN directed d ON d.mid = ac.mid WHERE
 g.genre = \'Action\' AND d.fname = \'Steven\' AND d.lname = \'Spielberg\'));
'''

# cursor = connection.cursor()
# cursor.execute("SELECT count(*) from ((SELECT a.id, a.fname, a.lname FROM actor a) EXCEPT (SELECT DISTINCT ac.id, ac.fname, ac.lname FROM actor_casts ac JOIN genre g ON ac.mid = g.mid JOIN directed d ON d.mid = ac.mid WHERE g.genre = \'Action\' AND d.fname = \'Steven\' AND d.lname = \'Spielberg\'));")
# all_rows = cursor.fetchall()
# print(f"Fetched all rows: {all_rows}")

def get_query_tokens_and_vals(query):
    parser = Parser(query)
    parsed_query = sqlparse.parse(query)
    tokens = []
    vals = []
    for i in range(len(parsed_query)):
        for token in parsed_query[i].flatten():
            if not token.is_whitespace: #only record non-whitespace tokens
                tokens.append(str(token.ttype))
                vals.append(str(token.normalized))
                print(f"Token: {repr(token.normalized)}, Type: {token.ttype}")
    return tokens, vals, parser

def extract_where_conditions(tokens, vals):
    conditions = []
    relns = []
    base_relns = {}
    for i in range(len(tokens)):
        #check for table aliasing, and update the base_relns dict
        # if i+1 < len(tokens): 
        #     if tokens[i] == 'Token.Name' and tokens[i+1] == 'Token.Name':
        #         base_relns[vals[i]] = vals[i]
        #         base_relns[vals[i+1]] = vals[i]
        #     elif i+2 < len(tokens):
        #         if(tokens[i] == 'Token.Name' and tokens[i+1] == 'Token.Keyword' and tokens[i+2] == 'Token.Keyword') and vals[i+1].lower == 'as':
        #             base_relns[vals[i]] = vals[i]
        #             base_relns[vals[i+2]] = vals[i]
        #gather where conditions
        if i+2 < len(tokens):
            if(tokens[i] == 'Token.Name' and tokens[i+1] == 'Token.Keyword' and tokens[i+2] == 'Token.Keyword') and vals[i+1].lower == 'as':
                base_relns[vals[i]] = vals[i]
                base_relns[vals[i+2]] = vals[i]



sql = "SELECT count(*) from ((SELECT a.id, a.fname, a.lname FROM actor a) EXCEPT (SELECT DISTINCT ac.id, ac.fname, ac.lname FROM actor_casts ac JOIN genre g ON ac.mid = g.mid JOIN directed d ON d.mid = ac.mid WHERE g.genre = \'Action\' AND d.fname = \'Steven\' AND d.lname = \'Spielberg\'));"
sql = "(SELECT DISTINCT ac.id, ac.fname, ac.lname FROM actor_casts ac JOIN genre g ON ac.mid = g.mid JOIN directed d ON d.mid = ac.mid WHERE g.genre = \'Action\' AND d.fname = \'Steven\' AND d.lname = \'Spielberg\');"
# sql = 'SELECT a.uniquely_named_col_from_a, b.uniquely_named_col_from_b FROM a JOIN b ON a.id = b.id;' #example where the parser retrieves aliases that do not exist
# extracted_conditions = extract_where_conditions(sql)
# print(extracted_conditions)
tokens, vals, parser = get_query_tokens_and_vals(sql)
print(tokens)
print(vals)
print(f"Tables found: {parser.tables}")
print(f"Columns found: {parser.columns}") # This is a list of all columns
print(f"Table aliases: {parser.tables_aliases}")
# print(tokens)

# st.title("Hello Streamlit-er 👋")
# st.markdown(
#     """ 
#     This is a playground for you to try Streamlit and have fun. 

#     **There's :rainbow[so much] you can build!**
    
#     We prepared a few examples for you to get started. Just 
#     click on the buttons above and discover what you can do 
#     with Streamlit. 
#     """
# )

# if st.button("Send balloons!"):
#     st.balloons()