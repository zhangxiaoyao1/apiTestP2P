from bs4 import BeautifulSoup

html = """
<html>
<head> <title>黑马程序员</title></head>
<body>
<p id="test01">软件测试</p>
<p id="test02">2020年</p>
<a href="/api.html">接口测试</a>
<a href="/web.html">Web自动化测试</a>
<a href="/app.html">APP自动化测试</a> 
</body>
</html>
"""

soup = BeautifulSoup(html, 'html.parser')

# 获取title的对象
print(soup.title)
# 获取title的标签名称
print(soup.title.name)
# 获取title的值
print(soup.title.string)

# 获取p的对象
print(soup.p)
# 获取所有的p的对象
print(soup.find_all('p'))

# 获取第一个p标签对应的ID属性的值

print(soup.p['id'])

# 一次打印出所有A标签的href属性的值和A标签的值
for s in soup.find_all('a'):
    print("href={} text={}".format(s['href'], s.string))
