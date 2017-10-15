import re
pattern=re.compile(r'Query Result:\s([a-zA-Z]+)_([a-zA-Z]+)_(\d+\.\d+\.\d+\.\d+\:\d+)_(\d+)')
s="dasjdsadjhsajkQuery Result: zxt_dxx_2017.10.15.14:53_1 67"
# pattern=re.compile(r'\d+\.\d+\.\d+\.\d+\:\d+')
# s="2017.10.15.14:53"
# print(re.search(pattern,s))
result=re.search(pattern,s)
print(result.group(1),result.group(2),result.group(3),result.group(4))