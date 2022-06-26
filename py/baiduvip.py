# _*_ coding: utf-8 _*_



import requests

cookies = {
    'BDUSS': 'lE1My1PMmdOZkoyN0pXNDV5Sjl5b0NNS1VrYkJaZWlsU2Q0ZmdJTkRWZUIteGxnRVFBQUFBJCQAAAAAAAAAAAEAAABjTxoPMjE1Njg5OTk5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIFu8l-BbvJfV',
    'BDUSS_BFESS': 'lE1My1PMmdOZkoyN0pXNDV5Sjl5b0NNS1VrYkJaZWlsU2Q0ZmdJTkRWZUIteGxnRVFBQUFBJCQAAAAAAAAAAAEAAABjTxoPMjE1Njg5OTk5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIFu8l-BbvJfV',
    'BAIDUID': '6E098D533FFA7B41028CC1277ECF8429:FG=1',
    'BIDUPSID': '6E098D533FFA7B41028CC1277ECF8429',
    'PSTM': '1609727727',
    '__yjs_duid': '1_a30e71a03f3317721f3603c4544497f91609745333512',
    '_click_param_reader_query_ab': '3',
    '_click_param_pc_rec_doc_2017_testid': '4',
    'MCITY': '-131%3A',
    'H_PS_PSSID': '',
    'BDORZ': 'FFFB88E999055A3F8A630C64834BD6D0',
    'Hm_lvt_f06186a102b11eb5f7bcfeeab8d86b34': '1612151861',
    'delPer': '0',
    'PSINO': '1',
    'BAIDUID_BFESS': '7A8DACD61F297AFCD7AB693029B6F4F5:FG=1',
    'ZD_ENTRY': 'baidu',
    'Hm_lpvt_f06186a102b11eb5f7bcfeeab8d86b34': '1612159934',
    'close_cashier_time_3_edf0938aad16350902788496f6362a16': '2',
    'ab_sr': '1.0.0_NmZmOWEyZmJmYTdiZWRiNjdmOTBmZDg0MDIxZTUzZjJkNWE0MjlmYWVlZDU5OGFiYmY2N2I1Zjc1NDMxZGY4NTdhN2YxZGYzNGNmN2I3MmU5MmEzZTUyOTk2ZGZkY2ZlNjM3NmU4MjU4YzM2MmI0NDY0N2I1NTU0ZDAzYmRjNzg=',
    'bcat': '0bf73fab643b4f1eb50cc7641147250281277fe9d8ade59827b1f05ee32069f602b6153eaa257e173a7a92da946ba624eb27531e4c0d38232582c6b609bed7b53000d7cc53ef98e5b5c4ec2345633d161e86039c04342d9d70c71996e5e2ed27220ddc5ea4fc7f0f958dab7f96ea0a82669cbd0783417895a7006532327fa663b1c3f9dc6e020511586262f0ff60b508',
    'LoseUserAllPage': '%7B%22type%22%3A0%2C%22status%22%3A0%2C%22expire_time%22%3A0%2C%22create_time%22%3A1612159943%2C%22cookie_time%22%3A1612246343%7D',
    'Hm_lvt_d8bfb560f8d03bbefc9bdecafc4a4bf6': '1612151871,1612152267,1612152384,1612159994',
    'Hm_lpvt_d8bfb560f8d03bbefc9bdecafc4a4bf6': '1612159994',
}

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Accept': 'application/json, text/plain, */*',
    'Cache-Control': 'no-cache, no-store',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://wenku.baidu.com/view/b34f3f8953ea551810a6f524ccbff121dd36c589.html',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

params = (
    ('query', 'S5700\u4EA4\u6362\u673A\u521D\u59CB\u5316\u548C\u914D\u7F6E'),
    ('essquery', 's5700\u4EA4\u6362\u673A\u914D\u7F6E'),
    ('eidStr', '20001'),
    ('url', 'https://wenku.baidu.com/view/b34f3f8953ea551810a6f524ccbff121dd36c589.html#'),
)

html = requests.get('https://wenku.baidu.com/ndview/interface/hx/fc', headers=headers, params=params, cookies=cookies).content.decode('utf-8')

print(html)


