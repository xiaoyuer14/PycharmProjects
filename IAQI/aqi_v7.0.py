"""	功能：AQI计算	日期：25/01/2019	版本： 7.0	os模块		提供与系统、目录操作相关的功能，不受平台限制		os.remove()             删除文件		os.makedirs()           删除多层目录		os.rmdir()              删除单级目录		os.rename()             重命名文件		os.path.isfile()        判断是否为文件		os.path.isdir()         判断是否为目录		os.path.join()          连接目录，如path1 连接 path2 为 path1/path2		os.path.splitext()      将文件分割成文件名和扩展名，如tmp.txt 分割为 tmp 和 .txt （可用于判断文件类型）	ps：with语句打开文件不需要关闭文件，会自动关闭	网络爬虫爬取实时数据	requests模块		是一个简洁且简单的处理http请求的工具		支持丰富的链接访问功能，包括url获取，http会话，cookie记录等		requests网页请求：		get()               对应的HTTP的GET方式		post()              对应HTTP的POST方式，用于传递用户数据		request对象属性：		status_code         HTTP请求的返回状态码		text                HTTP相应内容的字符串形式，即url对应的网页内容	beautifulSoup		用于解析HTML或XML		pip install beautifulsoup4		import bs4		步骤		1、创建BeautifulSoup对象		2、查找节点			find        找到第一个满足的节点			findall     找到所有满足的节点		eg： bs = BeautifulSoup(					url,					html_parser,    #指定解析器					enoding         #指定编码格式，确保和网页编码格式一致			)			bs.find_all('a',href='a.html')			bs.find_all('a', class_='a_link')  {'class': 'a_link'}"""import requestsfrom bs4 import BeautifulSoupimport csvdef get_city_aqi(city_pinyin):	"""		获取城市aqi	"""	url = 'http://pm25.in/' + city_pinyin	r = requests.get(url, timeout=30)	# print(r.status_code)	# soup = BeautifulSoup(r.text, 'lxml')	soup = BeautifulSoup(r.text, 'html.parser')	div_list = soup.find_all('div', {'class': 'span1'})	city_aqi = []	for i in range(8):		div_content = div_list[i]		caption = div_content.find('div', {'class': 'caption'}).text.strip()		value = div_content.find('div', {'class': 'value'}).text.strip()		city_aqi.append((caption, value))	return city_aqidef get_all_citys():	city_list = []	url = 'http://pm25.in/'	r = requests.get(url, timeout=30)	soup = BeautifulSoup(r.text, 'html.parser')	city_div = soup.find_all('div', {'class': 'bottom'})[1]	city_link_list = city_div.find_all('a')	for city_link in city_link_list:		city_name = city_link.text		city_pinyin = city_link['href'][1:]		city_list.append((city_name, city_pinyin))	return city_listdef write_to_csv(city_aqi_list, city_name_list):	filepath = 'citys_aqi.csv'	# lines = []	head_list = ['city']	for aqi_info in city_aqi_list[0]:		head_list.append(aqi_info[0])	# lines.append(head_list)	# for i in range(len(city_aqi_list)):	# 	line = [city_name_list[i]]	# 	for aqi in city_aqi_list[i]:	# 		line.append(aqi[1])		# lines.append(line)	with open( filepath, 'w', encoding='utf-8', newline='') as f :		writer = csv.writer(f)		writer.writerow(head_list)		for i in range( len( city_aqi_list ) ) :			line = [ city_name_list [ i ] ]			for aqi in city_aqi_list [ i ] :				line.append( aqi [ 1 ] )			writer.writerow(line)	# f = open( filepath , 'w' , encoding='utf-8' , newline='' )	# writer = csv.writer( f )	# for line in lines :	# 	# csv写文件	# 	writer.writerow( line )	# # csv读文件	# # ff = csv.reader(f)	# # print("读出来的：", ff)	#	# f.close( )	print("导出到{}成功，感谢使用，再见！".format(filepath))def main():	city_aqi_list = []	city_name_list = []	city_list = get_all_citys()	# i = 0	for city in city_list:		# if i > 1:		# 	break		# i += 1		city_name = city[0]		city_pinyin = city[1]		print('获取{}的aqi数据......'.format(city_name))		city_aqi = get_city_aqi(city_pinyin)		city_aqi_list.append(city_aqi)		city_name_list.append(city_name)		# print("****************** begin ******************")		# print('城市： {}'.format(city_val))		# print(' 空气质量AQI为:  {}'.format(aqi_val))		# print('    PM2.5/1h为:  {}'.format(pm25_1h_val))		# print('空气质量级别为:  {}'.format(level_val))		# print("******************  end  ******************")		# print()	write_to_csv(city_aqi_list, city_name_list)	# print("感谢使用，再见！")if __name__ == '__main__':	main()