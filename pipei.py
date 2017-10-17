import re


# s='Query Result: zxt_xsw_2017.10.16.11:35_3'
# pattern=re.compile(r'Query Result:\s([\b\w*\b]+)_([\b\w*\b]+)_(\d+\.\d+\.\d+\.\d+:\d+)_(\d+)')
s='result: status:200 payload:"zxt_xsw_2017.10.16.9:35_1,zxt_xsw_2017.10.16.10:35_2"'
pat1 = ".*result: status:200 payload:.*"
print(re.findall(pat1,s))