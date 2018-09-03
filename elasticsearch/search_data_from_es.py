from elasticsearch_dsl import connections, Search, FacetedSearch

if __name__ == '__main__':
    connections.create_connection(hosts=['localhost'])
    s = Search(index='test').query('match', title='题')
    response = s.execute()


    print(response)
    for one in response:
        print(one)
        print(one.title)
