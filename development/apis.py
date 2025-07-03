api_list = [
    # "AIzaSyCgr0Af_ph5vvql_VXpyIwfumJOaehbLDo",  # vmphat.24
    "AIzaSyAAmXLg2yM3Ygz3B_HYC4fcE1iJDNFhxm0",  # pvminh
    "AIzaSyAB9vrQbQPxOp1tbYWN9hjmmmno-9uGwR0",  # ngocquynh
    "AIzaSyCArspeWWKenZy4QSQlpBIrUAnXCWPRr90",  # kiet
    "AIzaSyBMcY_CGvsXGJSOMu3vLfWsd4-qL0bQflg",  # franie
    "AIzaSyAL9WZ2mO88O6DuwivJJWK2oqcy9_UXBNQ",  # daniel
    "AIzaSyDrD1yVeRW85VxX433JKFxKbtFuQ83UhMo",  # tulin
    "AIzaSyA8DDmJgizVgSiE2MdjnVpDZEXqTjEgBRg",  # martin

    # "AIzaSyAcvcAtAlMW4QD1OzCoIsmZl04qjFZ_AZo",  # khdludteam5
    # "AIzaSyCbs_KHkUr-BWL9X6_06kZb3brG7UI1a6w",  # vmphat21

    "AIzaSyBrTgG4YDzJMuK9WknMTbdnnoskSX1nvMY",  # pr

    # "AIzaSyDyjL0w1m1dWCNOP7_9UYXDQnNOqbAdbCw",  # vmphat.24
    "AIzaSyAHiAgc7tIuq4YKtswB-AaHa0W9eqQ5jGw",  # [v] pvminh
    "AIzaSyCnUToo7FRJn8v3BwMOt3FWwrDDFf2b4UI",  # [v] ngocquynh
    "AIzaSyCAnhUoYz6YAYCSfSFF-JmGNbMdxzhDKYU",  # kiet
    "AIzaSyBqu4Xbby4sc0vsCUbxhjqYcqOwKKAwaT4",  # franie
    "AIzaSyDh32FdRtHzuRUaZUXafcmlPHqYQtbRx3A",  # daniel
    "AIzaSyBRhc3Q6rdz3Ok93V5xB76Lfk3mNtdzQEI",  # tulin
    "AIzaSyDPUFWmBABBPAYEa_lOkeony8C2eqKkXTw",  # martin
    "AIzaSyAY8nfoP7DXfL571ovT8V_HlMWCTdHqdgc",  # khdludteam5
    "AIzaSyC4WprE1HsmCUwOoGi4HFfA1Lzg5XSE0Cg",  # vmphat21

    "AIzaSyC-letXWg8hVdOA8H6BlEXb-TXF7W7twQM",
    "AIzaSyCmJQlfuGKf2FNvrUWYd-fPuxYRcmm3p4Q",
    "AIzaSyDlKoywc1dVIaiv4UGVDc0OuaEBFluS2IU",
    "AIzaSyDk5UZkrHP6H3fgAI0FidWJKcVptQdEWBE",
    "AIzaSyBkVUkCK_mMBhJnyi9KoZ9WFf1tfJnlOac",
    "AIzaSyATHBdVQsH-7J8M2v6UcciZyWbzkr13uTA",
    "AIzaSyAvAt0as8Zs0r_iustkbWyimOhdLOzCm8w",
    "AIzaSyDaUPT6NQS8sqs16_hm9_A8ONHsVbh8QiY",


    "AIzaSyAdbNfxlQQQjKSgAcOjQt-XUwil-FMl6V8",  # [v] Luc - Ca nhan
    "AIzaSyCSGNpc1IlacTUwN31TKWms0RzF_we17vk",  # [v] Luc - Truong

    "AIzaSyBE8VObttX0oOGz5Jd82AtOiLTSzavIBL8",
    "AIzaSyAo5sCKOhGgYNgJ0m1QKsT29Ov-GNQHeSo",
    "AIzaSyDLa5CYtBGeXoV1-8y_ojA9eR_xzONABew",
    "AIzaSyCUtzli8ZRql653-0u_RrL7zM2SgEdb5ss",
    "AIzaSyBPi15fdt_YtyqaBIEuvSQ66T6T0ROHEA4",
    "AIzaSyC3DhYcDb8sLzzwywoJe8Foki3kMnVKPwQ",
    "AIzaSyDRE-VA4R9-UBRekhCGCcy3NlhlwQa1fnU",
    "AIzaSyD-WsC4RABxdqebovU-TYMueMHxPT2l6Nw",

    "AIzaSyDBscWgL9o2QtfNvx_xnZP3CWweyknGJKM",  # han-asd
    "AIzaSyAhbb5IEibxRDH8a8XB8Zk7lopPh8jhgwI",  # han-len
]

assert len(api_list) == len(set(api_list)), "Duplicate API keys found"
n_apis = len(api_list)
api_request_threshold = 1
api_idx = 0
