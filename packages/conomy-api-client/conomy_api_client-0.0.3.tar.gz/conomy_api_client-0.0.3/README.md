Conmy Data Api Client for Python
===================

Installation:

    pip install conomy_data_client

Usage

    from conomy_data_client import DataClient

    token = 'lalalalalalala'
    dc = DataClient(token) 

    issuers = cd.get_issurs()    # return list of issuers
