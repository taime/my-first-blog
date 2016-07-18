domain = "http://moscross.ru/"


# Получаем ссылки на коллекции всех фирм (из левого столбика)
def getLinks(url):
	url = 'http://moscross.ru/catalog/nike'
	from grab import Grab
	g = Grab(log_file='links.html')
	g.go(url)
	elements = g.doc.select('//div[@class="cats4 w"]/ul/li//div[@class="R"]/ul/li/a')
	links = []

	for elem in elements:
		links.append(elem.attr('href'))

	return links


def fixImageUrl(url):
	url = url.replace("/s/", "/l/")
	url = 'http://moscross.ru/'+url
	return url

# Получаем SRC всех картинок ВСЕХ объектов находящихся на странице c переданным url
def getProductsImages(url):
	from grab import Grab
	g = Grab(log_file='productsImages.html')
	g.go(url)

	products = g.doc.select('//div/div/div/div/div[@class="catalog w"]/div[@class="items fix"]/div[@class="item"]/h3/a')
	products_href = []
	products_images = []      
	for elem in products:
		href = elem.attr('href')
		href = 'http://moscross.ru/'+href
		products_href.append(href)

	for elem in products_href:
		products_images.append(getProductImages(elem))


	return products_images


# Парсим страничку коллекции и достаем ссылки на конкретные товар
def parseCollection(url):
	from grab import Grab
	g = Grab(log_file='collection.html')
	g.go(url)

	products = g.doc.select('//div[@class="catalog w"]//div[@class="items fix"]/div[@class="item"]/h3/a')
	product_links = []

	for elem in products:
		product_links.append(elem.attr("href"))

	return product_links

#Собираем все ссылки на продукты из всех каталогов
def parseCollections(catalog_collection_links):
	products_urls=[]
	for elem in catalog_collection_links:
		products_urls = products_urls + parseCollection(elem)
	return products_urls


# Получаем всю инфу о продукте
def getProduct(product_page_url):
	from grab import Grab
	g = Grab(log_file='product.html')
	g.go(product_page_url)
	pr = ''

	# Получаем URL Картинок
	product = g.doc.select('//div[@class="product w item"]/div[@class="L"]/div[@class="album"]/a/img')
	if len(product) > 0:
		images_list = []
		for image in product:
		    src = image.attr('src')
		    src = fixImageUrl(src)
		    images_list.append(src)
		images_str = ', '.join(images_list)
	
	else:
		product2 = g.doc.select('//div[@class="product w item"]/div[@class="L"]/div/a/img')
		images_str = product2.attr('src')
		images_str = fixImageUrl(images_str)
	pr_images = images_str

	#Находим имя
	pr_name = g.xpath_text('//div[@class="product w item"]/div[@class="R"]/h1')

	#Находим ОПИСАНИЕ
	pr_descr = g.xpath_text('//div[@class="product w item"]/div[@class="R"]/div[@class="text"]')
	pr_descr = pr_descr.replace(";",',')
	pr_descr = pr_descr.replace("Как определить размер...","")

	#Находим Размеры
	if g.search(u'<div class="param"><span>Размер</span>'):
		pr_sizes_first = g.doc.select('//div[@class="product w item"]/div[@class="R"]/div[@class="actions"]/div[@class="param"]/select/option').text()
		pr_sizes_last = g.doc.select('//div[@class="product w item"]/div[@class="R"]/div[@class="actions"]/div[@class="param"]/select/option[last()]').text()
		pr_sizes = '[Размер: '+pr_sizes_first[0:2] +'-'+ pr_sizes_last[0:2]+']'
	else:
		pr_sizes ='[Рамзер отсутствует]'


	#Находим цену
	if g.search(u'class="oldprice text"') and g.search(u'<div class="price">Цена:'):
		pr_oldprice = g.doc.select('//div[@class="product w item"]/div[@class="R"]/div/div[@class="oldprice text"]').number()
		pr_price = g.doc.select('//div[@class="product w item"]/div[@class="R"]/div/div[@class="price"]').number()
		pr_dif = pr_oldprice - pr_price
	else :
		pr_dif = 0
		pr_price = 0
		pr_oldprice = 0


	#Находим Катеогрию
	pr_category = g.doc.select('//div[@class="product w item"]/div[@class="uppercats"]/a[last()]').text()

	pr = 'Nike; Nike, '+ pr_category +'; ' +pr_name +pr_sizes+ '; '+pr_images+';'+str(pr_oldprice)+';'+str(pr_dif)+';'+pr_descr
	# pr = pr_category+ '; ' +pr_name + '; '+pr_images+';'+pr_descr
	return pr 


def getProducts(products_page_urls):
	# products_page_urls = giveAllProductsLinks()
	# products_page_urls = ['item/309-nike-roshe-run-016',
	# 'item/932-krossovki-nike-roshe-run-art046',]
	products = []
	for url in products_page_urls:
		product = getProduct(url)
		products.append(product)

	return products


#добавляем в начало ссылки домен (для относительных ссылок)
def addDomain(url_list):
	new_url_list = [domain+url for url in url_list]
	return new_url_list


newbalance_collections = ['catalog/new-balance-574',
          'catalog/new-balance-576',
          'catalog/new-balance-577',
          'catalog/new-balance-580',
          'catalog/new-balance-670',
          'catalog/new-balance-990',
          'catalog/new-balance-996',
          'catalog/new-balance-998',
          'catalog/new-balance-999',
          'catalog/new-balance-1400',]
newbalance_collections = addDomain(newbalance_collections)


nike_collections = ['catalog/nike-roshe-run',
	'catalog/nike-air-max-90',
	'catalog/nike-air-force',
	'catalog/nike-free-run',
	'catalog/nike-air-max-95-new',
	'catalog/nike-huarache',
	'catalog/nike-air-max-87',
	'catalog/nike-air-max-zero',
	'catalog/nike-air-max-2017',
	'catalog/nike-air-max-2016',
	'catalog/nike-air-max-2015',
	'catalog/nike-air-max-2014',
	'catalog/nike-air-max-vt',
	'catalog/nike-air-max-90-hyperfuse',
	'catalog/nike-skyline',
	'catalog/nike-i',
	'catalog/nike-thea',
	'catalog/air-jordan',
	'catalog/cortez',
	'catalog/nike-flyknit-',
	'catalog/nike-lebron',
	'catalog/nike-lunar',
	'catalog/nike-air-max-90-sneakerboot',
	'catalog/nike-flystepper-2k3-prm-qs',
	'catalog/nike-sock',
	'catalog/stefan-janoski-']
nike_collections = addDomain(nike_collections)

adidas_collections = ['catalog/adidas-super-star',
	'catalog/adidas-yeezy-boots-350',
	'catalog/adidas-nmd-runner',
	'catalog/adidas-zx-runner',
	'catalog/adidas-hamburg',
	'catalog/adidas-y-3',
	'catalog/Adidas-Equipment',
	'catalog/adidas-zx-750',
	'catalog/adidas-zx-flux',
	'catalog/adidas-porsche-design',
	'catalog/adidas-ransom',
	'catalog/adidas-springblade',
	'catalog/adidas-tubular',
	'catalog/adidas-marathon-flyknit',
	'catalog/adidas-stan-smith',
	'catalog/adidas-spring-bounce-']
adidas_collections = addDomain(adidas_collections)




nike_links = ['item/309-nike-roshe-run-016',
	'item/932-krossovki-nike-roshe-run-art046',
	'item/841-krossovki-nike-roshe-run-art032',
	'item/917-krossovki-nike-roshe-run-art045',
	'item/933-krossovki-nike-roshe-run-art047',
	'item/797-krossovki-nike-roshe-run-art030',
	'item/866-krossovki-cem-cvetov-art101',
	'item/998-krossovki-nike-roshe-run-art055',
	'item/979-krossovki-nike-roshe-run-art054',
	'item/795-krossovki-nike-roshe-run-art028',
	'item/299-nike-roshe-run-007',
	'item/967-krossovki-nike-roshe-run-art051',
	'item/914-krossovki-nike-roshe-run-art044',
	'item/891-krossovki-nike-roshe-run-art043',
	'item/304-nike-roshe-run-011',
	'item/298-nike-roshe-run-005',
	'item/934-krossovki-nike-roshe-run-art048',
	'item/1217-krossovki-nike-roshe-run-art073',
	'item/314-nike-roshe-run-020',
	'item/1201-krossovki-nike-roshe-run-art072',
	'item/306-nike-roshe-run-013',
	'item/1053-krossovki-nike-roshe-run-art061',
	'item/296-nike-roshe-run-003',
	'item/312-nike-roshe-run-018',
	'item/969-krossovki-nike-roshe-run-art052',
	'item/794-krossovki-nike-roshe-run-art027',
	'item/1059-krossovki-nike-roshe-run-art062',
	'item/305-nike-roshe-run-012',
	'item/313-nike-roshe-run-019',
	'item/54-nike-air-max-2014-021',
	'item/1123-krossovki-nike-air-max-90-art075',
	'item/70-nike-air-max-90-009',
	'item/72-nike-air-max-90-011',
	'item/1076-krossovki-nike-air-max-90-art073',
	'item/73-nike-air-max-90-012',
	'item/66-nike-air-max-90-005',
	'item/82-nike-air-max-90-020',
	'item/1075-krossovki-nike-air-max-90-art072',
	'item/2002-krossovki-nike-air-max-90-temno-sinijj-dark-blue-art084',
	'item/695-krossovki-nike-air-max-90-chernyjj-black-art019',
	'item/892-krossovki-nike-air-max-90-art050',
	'item/2003-krossovki-nike-air-max-90-bordovyjjseryjj-bordogray-art085',
	'item/78-nike-air-max-90-017',
	'item/76-nike-air-max-90-015',
	'item/69-nike-air-max-90-008',
	'item/79-nike-air-max-90-018',
	'item/1054-krossovki-nike-air-max-90-chernyjjbelyjj-blackwhite-art071',
	'item/940-krossovki-nike-air-max-90-art059',
	'item/75-nike-air-max-90-014',
	'item/894-krossovki-nike-air-max-90-art052',
	'item/692-krossovki-nike-air-max-90-art046',
	'item/1767-krossovki-nike-air-max-90-art080',
	'item/673-nike-air-max-90-belyjjrozovyjj-art031',
	'item/65-nike-air-max-90-004',
	'item/62-nike-air-max-90',
	'item/64-nike-air-max-90-003',
	'item/910-krossovki-nike-air-max-90-art057',
	'item/74-nike-air-max-90-013',
	'item/689-krossovki-nike-air-max-90-art043',
	'item/92-nike-air-force-001',
	'item/679-krossovki-nike-air-force-1-low-art007',
	'item/96-nike-air-force-005',
	'item/316-nike-air-force-010',
	'item/94-nike-air-force-003',
	'item/93-nike-air-force-002',
	'item/757-krossovki-nike-air-force-1-low-art015',
	'item/1180-krossovki-nike-air-force-art044',
	'item/140-nike-air-force-009',
	'item/97-nike-air-force-006',
	'item/129-nike-free-run-003',
	'item/291-nike-free-run-011',
	'item/905-krossovki-nike-free-run-30-art035',
	'item/555-nike-free-run-50-026',
	'item/130-nike-free-run-004',
	'item/128-nike-free-run-002',
	'item/127-nike-free-run-001',
	'item/556-nike-free-run-50-027',
	'item/908-krossovki-nike-free-run-30-art038',
	'item/919-krossovki-nike-free-run-30-art040',
	'item/nike-free-run-023',
	'item/960-krossovki-nike-free-run-fit-art044',
	'item/959-krossovki-nike-free-run-fit-art043',
	'item/904-krossovki-nike-free-run-30-art034',
	'item/557-nike-free-run-50-028',
	'item/334-nike-free-run-3-50-016',
	'item/1079-krossovki-nike-free-art046',
	'item/492-nike-free-30-v5-012',
	'item/1744-krossovki-nike-air-max-95-art014-belyjjchernyjj-whiteblack',
	'item/1651-nike-air-max-95-art001',
	'item/1748-krossovki-nike-air-max-95-art018-belyjjmnogocvetnyjj-whitemulticolor',
	'item/1746-krossovki-nike-air-max-95-art016-chernyjjtemno-sinijj-blackdark-blue',
	'item/krossovki-nike-air-max-95-art010-',
	'item/1675-nike-air-max-95-art008',
	'item/1760-krossovki-nike-air-max-95-art019',
	'item/1674-nike-air-max-95-art007',
	'item/1747-krossovki-nike-air-max-95-art017-belyjjseryjjoranzhevyjj-whitegreyorange',
	'item/1673-nike-air-max-95-art006',
	'item/1886-krossovki-nike-air-huarache-art046-golubojj-blue',
	'item/1888-krossovki-nike-air-huarache-art048-oranzhevyjj-orange',
	'item/1885-krossovki-nike-air-huarache-art045-belyjj-white',
	'item/1884-krossovki-nike-air-huarache-art044-chernyjj-black',
	'item/1887-krossovki-nike-air-huarache-art047-seryjj-grey',
	'item/851-nike-huarache-art002',
	'item/853-nike-huarache-art004',
	'item/1153-nike-huarache-art014',
	'item/1997-krossovki-nike-air-huarache-art051-seryjj-grey',
	'item/1998-krossovki-nike-air-huarache-art052-chernyjj-black',
	'item/2000-krossovki-nike-air-huarache-art054-temno-sinijj-dark-blue',
	'item/1999-krossovki-nike-air-huarache-art053-chernyjj-black',
	'item/2001-krossovki-nike-air-huarache-art055-seryjj-grey',
	'item/860-nike-huarache-art005',
	'item/1954-krossovki-nike-air-huarache-art049-chernyjjkrasnyjjbelyjj-blackredwhite',
	'item/1955-krossovki-nike-air-huarache-art050-seryjj-grey',
	'item/1451-nike-air-huarache-art024',
	'item/900-nike-huarache-art007',
	'item/1331-nike-huarache-art019',
	'item/981-nike-huarache-art008',
	'item/1714-krossovki-nike-air-huarache-art033-chernyjjrozovyjjzelenyjj-blackpinkgreen',
	'item/1332-nike-huarache-art020',
	'item/861-nike-huarache-art006',
	'item/1449-nike-air-huarache-art022',
	'item/852-nike-huarache-art003',
	'item/1149-nike-huarache-art010',
	'item/1455-nike-air-huarache-art028',
	'item/1150-nike-huarache-art011',
	'item/1716-krossovki-nike-air-huarache-art034',
	'item/1726-krossovki-nike-air-huarache-art036-krasnyjjred',
	'item/150-nike-air-max-87-010',
	'item/142-nike-air-max-87-002',
	'item/1750-krossovki-nike-air-max-87-art080-chernyjj-black',
	'item/1752-krossovki-nike-air-max-87-art082-belyjj-white',
	'item/1749-krossovki-nike-air-max-87-art079-chernyjjbelyjj-blackwhite',
	'item/1753-krossovki-nike-air-max-87-art083-temno-sinijj-dark-blue',
	'item/1755-krossovki-nike-air-max-87-art084-belyjjbiryuzovyjj-whiteturquoise',
	'item/922-krossovki-nike-air-max-87-chernyjjbelyjj-blackwhite-art045',
	'item/1751-krossovki-nike-air-max-87-art081-chernyjjbelyjj-blackwhite',
	'item/1539-krossovki-nike-air-max-90-art078',
	'item/163-nike-air-max-87-023',
	'item/866-krossovki-cem-cvetov-art101',
	'item/160-nike-air-max-87-020',
	'item/819-krossovki-nike-air-max-87-vishnyovyjjart040',
	'item/818-krossovki-nike-air-max-87-serofioletovyjj-art039',
	'item/817-krossovki-nike-air-max-87-fioletovyjj-art038',
	'item/153-nike-air-max-87-013',
	'item/152-nike-air-max-87-012',
	'item/1211-krossovki-nike-air-max-87-belyjjtemno-sinijj-whitedark-blue-art048',
	'item/164-nike-air-max-87-024',
	'item/144-nike-air-max-87-002',
	'item/141-nike-air-max-87-001',
	'item/166-nike-air-max-87-026',
	'item/143-nike-air-max-87-003',
	'item/146-nike-air-max-87-006',
	'item/145-nike-air-max-87-005',
	'item/151-nike-air-max-87-011',
	'item/147-nike-air-max-87-007',
	'item/148-nike-air-max-87-008',
	'item/157-nike-air-max-87-017',
	'item/1927-krossovki-nike-air-max-zero-art001',
	'item/1929-krossovki-nike-air-max-zero-art003',
	'item/1930-krossovki-nike-air-max-zero-art004',
	'item/1931-krossovki-nike-air-max-zero-art005',
	'item/1932-krossovki-nike-air-max-zero-art006',
	'item/1933-krossovki-nike-air-max-zero-art007',
	'item/1928-krossovki-nike-air-max-zero-art002',
	'item/1190-krossovki-nike-air-max-2017-art019',
	'item/1188-krossovki-nike-air-max-2017-art017',
	'item/1189-krossovki-nike-air-max-2017-art018',
	'item/1764-krossovki-nike-air-max-2016-art020-sinijjkrasnyjjbluered',
	'item/1898-krossovki-nike-air-max-2016-art024-temno-sinijjrozovyjj-dark-bluepink',
	'item/1765-krossovki-nike-air-max-2016-art021-chernyjjsinijjzelyonyjj-blackbluegreen',
	'item/1238-nike-air-max-2016-art005',
	'item/1863-krossovki-nike-air-max-2016-art023',
	'item/1763-krossovki-nike-air-max-2016-art019',
	'item/1242-nike-air-max-2016-art009',
	'item/1243-krossovki-nike-air-max-2016-art010',
	'item/1241-nike-air-max-2016-art008',
	'item/1236-nike-air-max-2016-art003',
	'item/1240-nike-air-max-2016-art007',
	'item/1237-nike-air-max-2016-art004',
	'item/1719-krossovki-nike-air-max-2016-art015-',
	'item/1239-nike-air-max-2016-art006',
	'item/1234-nike-air-max-2016-art001',
	'item/1732-krossovki-nike-air-max-2016-art018',
	'item/1862-krossovki-nike-air-max-2016-art022-chernyjjrozovyjj-blackpink',
	'item/1595-krossovki-nike-air-max-2016-art012',
	'item/1662-krossovki-nike-air-max-2016-art013',
	'item/1663-krossovki-nike-air-max-2016-art014',
	'item/1559-krossovki-nike-air-max-2016-art010',
	'item/505-nike-air-max-2015-009',
	'item/2016-krossovki-nike-air-max-2015-art025',
	'item/54-nike-air-max-2014-021',
	'item/502-nike-air-max-2015-006',
	'item/672-nike-air-max-2015-014',
	'item/506-nike-air-max-2015-010',
	'item/54-nike-air-max-2014-021',
	'item/44-nike-air-max-2014-011',
	'item/42-nike-air-max-2014-008',
	'item/38-nike-air-max-2014005',
	'item/548-nike-air-max-2014-032',
	'item/57-nike-air-max-2014-024',
	'item/39-nike-air-max-2014-006',
	'item/40-nike-air-max-2014007',
	'item/58-nike-air-max-2014025',
	'item/545-nike-air-max-2014-029',
	'item/547-nike-air-max-2014-031',
	'item/546-nike-air-max-2014-030',
	'item/885-nike-air-max-2014-belyjj-zelenyjj-rozovyjj-art040',
	'item/48-nike-air-max-2014-015',
	'item/122-nike-air-max-90-vt-003',
	'item/123-nike-air-max-90-vt-004',
	'item/121-nike-air-max-90-vt-002',
	'item/124-nike-air-max-90-vt-005',
	'item/126-nike-air-max-90-vt-007',
	'item/110-nike-air-max-90-hyperfuse-012',
	'item/102-nike-air-max-90-hyperfuse-004',
	'item/114-nike-air-max-90-hyperfuse-016',
	'item/101-nike-air-max-90-hyperfuse-003',
	'item/104-nike-air-max-90-hyperfuse-006',
	'item/108-nike-air-max-90-hyperfuse-010',
	'item/866-krossovki-cem-cvetov-art101',
	'item/116-nike-air-max-90-hyperfuse-018',
	'item/99-nike-air-max-90-hyperfuse-001',
	'item/113-nike-air-max-90-hyperfuse-015',
	'item/107-nike-air-max-90-hyperfuse-009',
	'item/100-nike-air-max-90-hyperfuse-002',
	'item/112-nike-air-max-90-hyperfuse-014',
	'item/605-nike-skyline-013',
	'item/595-nike-skyline-002',
	'item/596-nike-skyline-003',
	'item/608-nike-skyline-016',
	'item/807-nike-skyline-art017',
	'item/599-nike-skyline-006',
	'item/1168-nike-skyline-art022',
	'item/1165-nike-skyline-art019',
	'item/588-nike-air-90-yeezy-2-009',
	'item/586-nike-air-makh-90-yeezy-2-007',
	'item/587-nike-air-90-yeezy-2-008',
	'item/585-nike-air-90-yeezy-2-006',
	'item/489-nike-izzy003',
	'item/1192-nike-air-90-yeezy-2-sp-art011',
	'item/485-nike-izzy001',
	'item/488-nike-izzy004',
	'item/1850-nike-air-90-yeezy-2-art018',
	'item/1851-nike-air-90-yeezy-2-art019',
	'item/1852-nike-air-90-yeezy-2-art020',
	'item/1854-nike-air-90-yeezy-2-art021',
	'item/1740-nike-air-90-yeezy-2-art017',
	'item/1735-nike-air-90-yeezy-2-art012',
	'item/1736-nike-air-90-yeezy-2-art013',
	'item/1737-nike-air-90-yeezy-2-art014',
	'item/1738-nike-air-90-yeezy-2-art015',
	'item/1739-nike-air-90-yeezy-2-art016',
	'item/29-nike-thea001',
	'item/31-nike-thea003',
	'item/30-nike-thea-002',
	'item/394-nike-air-jordan-07',
	'item/389-nike-air-jordan-02',
	'item/395-nike-air-jordan-008',
	'item/393-nike-air-jordan-06',
	'item/1122-nike-air-jordan-art015',
	'item/768-nike-air-jordan-003',
	'item/769-nike-air-jordan-010',
	'item/1407-nike-air-jordan-art031',
	'item/1593-nike-air-jordan-art038',
	'item/1162-nike-air-jordan-art021',
	'item/1592-nike-air-jordan-art037',
	'item/1665-nike-air-jordan-art040',
	'item/1591-nike-air-jordan-art036',
	'item/1494-nike-air-jordan-art035',
	'item/1493-nike-air-jordan-art034',
	'item/1492-nike-air-jordan-art033',
	'item/1218-nike-air-jordan-art023',
	'item/1219-nike-air-jordan-art024',
	'item/1220-nike-air-jordan-art025',
	'item/1221-nike-air-jordan-art026',
	'item/1222-nike-air-jordan-art027',
	'item/1223-nike-air-jordan-art028',
	'item/1224-nike-air-jordan-art029',
	'item/1225-nike-air-jordan-art030',
	'item/1128-nike-air-jordan-art017',
	'item/1127-nike-air-jordan-art016',
	'item/390-nike-air-jordan-03',
	'item/396-nike-air-jordan-09',
	'item/1096-nike-air-jordan-art013',
	'item/1095-nike-air-jordan-art012',
	'item/444-nike-cortez-190',
	'item/178-nike-cortez',
	'item/450-nike-cortez-196',
	'item/445-nike-cortez-191',
	'item/81-nike-air-max-2014-008',
	'item/36-nike-air-max-2014003',
	'item/Nike-FLYKNIT-',
	'item/700-nike-flyknit-art007',
	'item/837-nike-zoom-lebron-art005',
	'item/833-nike-zoom-lebron001',
	'item/834-nike-zoom-lebron-art001',
	'item/835-nike-zoom-lebron-art003',
	'item/708-nike-lunar-art001',
	'item/717-nike-lunar-art010',
	'item/713-nike-lunar-art006',
	'item/345-nike-air-max-90-sneakerboot-001',
	'item/347-nike-air-max-90-sneakerboot-003',
	'item/1232-nike-flystepper-2k3-art-001',
	'item/1233-nike-flystepper-2k3-art-002',
	'item/1993-nike-sock-dart-art007',
	'item/1994-nike-sock-dart-art008',
	'item/1996-nike-sock-dart-art010',
	'item/1050-nike-sock-dart-art005',
	'item/1051-nike-sock-dart-art006',
	'item/1032-nike-sock-art003',
	'item/1033-nike-sock-art004',
	'item/748-nike-stefan-janoski-art002',
	'item/749-nike-stefan-janoski-art003',
	'item/839-nike-stefan-janoski-art005',]
nike_links = addDomain(nike_links)

adidas_links = ['item/1012-krossovki-adidas-super-star-art-010',
	'item/1092-krossovki-adidas-super-star-art014',
	'item/1007-krossovki-adidas-super-star-art-005',
	'item/1006-krossovki-adidas-super-star-art-004',
	'item/1940-krossovki-adidas-super-star-art-022',
	'item/1005-krossovki-adidas-super-star-art-003',
	'item/1227-krossovki-adidas-super-star-art-021',
	'item/1003-krossovki-adidas-super-star-art-001',
	'item/1091-krossovki-adidas-super-star-art013',
	'item/1093-krossovki-adidas-super-star-art015',
	'item/1089-krossovki-adidas-super-star-art011',
	'item/1090-krossovki-adidas-super-star-art012',
	'item/183-nike-air-max-2014-106',
	'item/1004-krossovki-adidas-super-star-art-002',
	'item/1727-adidas-yeezy-boost-350-art022',
	'item/1072-adidas-yeezy-350-boost-low-art001',
	'item/1253-adidas-yeezy-350-boost-low-art013',
	'item/1074-adidas-yeezy-350-boost-low-art003',
	'item/2005-krossovki-adidas-yeezy-boost-350-art033',
	'item/2006-krossovki-adidas-yeezy-boost-550-art034',
	'item/2007-krossovki-adidas-yeezy-boost-550-art035',
	'item/1664-adidas-yeezy-boost-350-art019',
	'item/1904-adidas-yeezy-boost-350-art028',
	'item/1073-adidas-yeezy-350-boost-low-art002',
	'item/1900-adidas-yeezy-boost-350-art024',
	'item/1728-adidas-yeezy-boost-350-art023',
	'item/1905-adidas-yeezy-boost-350-art029',
	'item/1906-adidas-yeezy-boost-350-art030',
	'item/1907-adidas-yeezy-boost-350-art031',
	'item/1908-adidas-yeezy-boost-350-art032',
	'item/1861-adidas-yeezy-boost-350-art023',
	'item/1729-adidas-yeezy-boost-350-art021',
	'item/1730-adidas-yeezy-boost-350-art020',
	'item/1356-adidas-yeezy-boost-350-art015',
	'item/1383-adidas-kanye-west-seryjjgrayart002',
	'item/1962-adidas-nmd-runner-art007',
	'item/1963-adidas-nmd-runner-art008',
	'item/1913-adidas-nmd-runner-art004',
	'item/1910-adidas-nmd-runner-art001',
	'item/1915-adidas-nmd-runner-art006',
	'item/1911-adidas-nmd-runner-art002',
	'item/1914-adidas-nmd-runner-art005',
	'item/1230-adidas-zx-runner-art002',
	'item/1229-adidas-zx-runner-art001',
	'item/1231-adidas-zx-runner-art003',
	'item/2009-adidas-hamburg-art002',
	'item/2013-adidas-hamburg-art006',
	'item/2015-adidas-hamburg-art008',
	'item/2011-adidas-hamburg-art004',
	'item/2014-adidas-hamburg-art007',
	'item/2012-adidas-hamburg-art005',
	'item/2010-adidas-hamburg-art003',
	'item/2008-adidas-hamburg-art001',
	'item/759-y-3-art001',
	'item/854-y-3-art005',
	'item/761-y-3-art003',
	'item/1401-adidas-y-3-art010',
	'item/1403-adidas-y-3-art012',
	'item/1402-adidas-y-3-art011',
	'item/1444-adidas-running-art002',
	'item/1710-adidas-equipment-running-art013',
	'item/1495-adidas-running-art003',
	'item/1496-adidas-running-art004',
	'item/1497-adidas-running-art005',
	'item/2018-krossovki-adidas-zx-700-art337',
	'item/2019-krossovki-adidas-zx-700-art338',
	'item/1578-adidas-zx-750-art031',
	'item/876-adidas-zx-750-art001',
	'item/1058-adidas-zx-750-art009',
	'item/902-adidas-zx-750-art003',
	'item/1909-krossovki-adidas-zx-750-art336',
	'item/901-adidas-zx-750-art002',
	'item/1882-krossovki-adidas-zx-750-art335',
	'item/1137-adidas-zx-750-art013',
	'item/1066-adidas-zx-750-art010',
	'item/936-adidas-zx-750-art004',
	'item/1203-adidas-zx-750-art027',
	'item/1169-adidas-zx-750-art015',
	'item/1170-adidas-zx-750-art016',
	'item/1171-adidas-zx-750-art017',
	'item/1172-adidas-zx-750-art018',
	'item/1173-adidas-zx-750-art019',
	'item/1174-adidas-zx-750-art020',
	'item/1175-adidas-zx-750-art021',
	'item/1179-adidas-zx-750-art025',
	'item/1056-adidas-zx-750-art007',
	'item/1055-adidas-zx-750-art006',
	'item/1057-adidas-zx-750-art008',
	'item/1877-adidas-zx-flux-art018',
	'item/1878-adidas-zx-flux-art019',
	'item/1186-adidas-zx-flux-art017',
	'item/684-adidas-zx-flux-art015',
	'item/683-adidas-zx-flux-art010',
	'item/681-adidas-zx-flux-art012',
	'item/172-adidas-porsche-design-010',
	'item/171-adidas-porsche-design-009',
	'item/167-adidas-porsche-design-005',
	'item/168-adidas-porsche-design-006',
	'item/170-adidas-porsche-design-008',
	'item/754-adidas-porsche-design-art017',
	'item/755-adidas-porsche-design-art018',
	'item/138-adidas-porsche-design-004',
	'item/136-adidas-porsche-design-002',
	'item/137-adidas-porsche-design-003',
	'item/496-adidas-porsche-design-012',
	'item/1140-adidas-ransom-art001',
	'item/1141-adidas-ransom-art002',
	'item/1142-adidas-ransom-art003',
	'item/1984-adidas-springblade-art011',
	'item/1985-adidas-springblade-art012',
	'item/705-adidas-springblade-art003',
	'item/1958-adidas-springblade-art010',
	'item/704-adidas-springblade-art002',
	'item/703-adidas-springblade-art001',
	'item/1707-krossovki-adidas-tubular-art-016',
	'item/1706-krossovki-adidas-tubular-art-015',
	'item/1705-krossovki-adidas-tubular-art-014',
	'item/1704-krossovki-adidas-tubular-art-013',
	'item/1261-krossovki-adidas-tubular-art-010',
	'item/1260-krossovki-adidas-tubular-art-009',
	'item/1259-krossovki-adidas-tubular-art-008',
	'item/1258-krossovki-adidas-tubular-art-007',
	'item/1257-krossovki-adidas-tubular-art-006',
	'item/1959-adidas-marathon-flyknit-art008-chernyjjbelyjj-blackwhite',
	'item/1960-adidas-marathon-flyknit-art009-temno-sinijj-dark-blue',
	'item/1961-adidas-marathon-flyknit-art010-chernyjjkrasnyjjbelyjj-blackredwhite',
	'item/663-adidas-marathon-flyknitart006',
	'item/661-adidas-marathon-flyknitart004',
	'item/659-adidas-marathon-flyknitart002',
	'item/658-adidas-marathon-flyknitart001',
	'item/1779-kedy-vans-art001',
	'item/1781-kedy-vans-art003',
	'item/1780-kedy-vans-art002',
	'item/1979-adidas-spring-bounce-art001',
	'item/1980-adidas-spring-bounce-art002',
	'item/1981-adidas-spring-bounce-art003',
	'item/1982-adidas-spring-bounce-art004',
	'item/1983-adidas-spring-bounce-art005']
adidas_links = addDomain(adidas_links)

newbalance_links = ['item/1986-new-balance-574-art123',
          'item/1987-new-balance-574-art124',
          'item/1988-new-balance-574-art125',
          'item/1989-new-balance-574-art127',
          'item/1990-new-balance-574-art128',
          'item/1991-new-balance-574-art129',
          'item/1992-new-balance-574-art126',
          'item/1919-new-balance-574-art116-sinijjbelyjj-bluewhite',
          'item/984-krossovki-new-balance-574-chernyjjbelyjj-blackwhite-art045',
          'item/1935-new-balance-574-art119',
          'item/1937-new-balance-574-art121',
          'item/1938-new-balance-574-art122',
          'item/1936-new-balance-574-art120',
          'item/1934-new-balance-574-art118',
          'item/1921-new-balance-574-art117-rozovyjj-pink',
          'item/1891-krossovki-new-balance-574-art115-golubojj-blue',
          'item/618-new-balance-008',
          'item/911-krossovki-new-balance-574-sirenevyjj-lilac-art034',
          'item/639-new-balance-029',
          'item/1796-new-balance-574-art100-krasnyjj-red',
          'item/620-new-balance-010',
          'item/1757-krossovki-new-balance-574-chernyjjseryjjrozovyjj-blackgreypink-art086',
          'item/1795-new-balance-574-art099-seryjj-grey',
          'item/1808-new-balance-574-art112-chernyjjfioletovyjj-blackviolet',
          'item/1810-new-balance-574-art114-tyomno-sinijj-dark-blue',
          'item/1809-new-balance-574-art113-kremovyjj-cream',
          'item/1806-new-balance-574-art110-sinijj-blue',
          'item/1803-new-balance-574-art107-seryjj-light-grey',
          'item/1802-new-balance-574-art106-sinijj-blue',
          'item/1801-new-balance-574-art105-zelenye-green',
          'item/1099-krossovki-new-balance-576-art003',
          'item/1100-krossovki-new-balance-576-art004',
          'item/874-krossovki-new-balance-576-art041',
          'item/1816-new-balance-577-art5-korichnevyjj-brown',
          'item/1814-new-balance-577-art3-sinijj-blue',
          'item/1813-new-balance-577-art2-seryjj-grey',
          'item/1812-new-balance-577-art1-temno-sinijj-dark-blue',
          'item/1487-new-balance-580-art007',
          'item/1538-new-balance-580-art013',
          'item/1537-new-balance-580-art012',
          'item/1534-new-balance-580-art009',
          'item/1486-new-balance-580-art006',
          'item/1411-new-balance-580-art005',
          'item/1410-new-balance-580-art004',
          'item/1409-new-balance-580-art003',
          'item/1922-new-balance-670-art016',
          'item/1973-new-balance-670-art018',
          'item/1923-new-balance-670-art015',
          'item/1924-new-balance-670-art014-seryjj-grey',
          'item/1939-new-balance-670-art017',
          'item/1590-new-balance-670-art012',
          'item/1583-new-balance-670-art005',
          'item/1587-new-balance-670-art009',
          'item/1588-new-balance-670-art010',
          'item/1586-new-balance-670-art008',
          'item/1584-new-balance-670-art006',
          'item/1582-new-balance-670-art004',
          'item/1581-new-balance-670-art003',
          'item/1580-new-balance-670-art002',
          'item/1579-new-balance-670-art001',
          'item/1918-new-balance-990-art008',
          'item/1920-new-balance-990-art009',
          'item/918-new-balance-990-art001',
          'item/1821-new-balance-990-art7-krasnyjj-red',
          'item/1818-new-balance-990-art4-seryjj-grey',
          'item/1820-new-balance-990-art6-chernyjj-black',
          'item/1819-new-balance-990-art5-zelenyjj-green',
          'item/2017-krossovki-new-balance-996-sinijj-art068',
          'item/1974-krossovki-new-balance-996-art063',
          'item/1975-krossovki-new-balance-996-temno-sinijjchernyjj-dark-blueblack-art064',
          'item/1976-krossovki-new-balance-996-temno-sinijjchernyjj-dark-blueblack-art065',
          'item/1977-krossovki-new-balance-996-temno-sinijjbezhevyjj-dark-bluebeige-art066',
          'item/1978-krossovki-new-balance-996-zelenyjjseryjj-greengrey-art067',
          'item/923-krossovki-new-balance-996-seryjj-gray-art029',
          'item/1865-krossovki-new-balance-996-art057-krasnyjj-red',
          'item/1868-krossovki-new-balance-996-art058-korichnevyjj-brown',
          'item/1870-krossovki-new-balance-996-art059-temno-sinijj-dark-blue',
          'item/1873-krossovki-new-balance-996-art060-vishnevyjj-cherry',
          'item/1875-krossovki-new-balance-996-art061-sinijj-blue',
          'item/1876-krossovki-new-balance-996-art062-chernyjj-black',
          'item/635-new-balance-025',
          'item/1828-new-balance-996-art47-malinovyjj-raspberry',
          'item/1836-new-balance-996-art54-seryjj-grey',
          'item/1832-new-balance-996-art51-myatnyjj-mint',
          'item/1831-new-balance-996-art50-seryjj-grey',
          'item/1826-new-balance-996-art45-krasnyesinie-redblue',
          'item/1825-new-balance-996-art44-biryuzovye-turqiouse',
          'item/1823-new-balance-996-art42-krasnyjj-red',
          'item/1822-new-balance-996-art41-lajjm-lime',
          'item/1158-krossovki-new-balance-996-art037-svetlo-korichnevyjj-light-brown',
          'item/1157-krossovki-new-balance-996-art036-seryjj-grey',
          'item/955-krossovki-new-balance-996-krasnyjj-red-art033',
          'item/954-krossovki-new-balance-996-chernyjj-black-art032',
          'item/953-krossovki-new-balance-996-temno-seryjj-dark-grey-art031',
          'item/638-new-balance-028',
          'item/637-new-balance-027',
          'item/636-new-balance-026',
          'item/1838-new-balance-998-art46-toplenoe-moloko-baked-milk',
          'item/875-krossovki-new-balance-998-art042',
          'item/873-krossovki-new-balance-998-art040',
          'item/871-krossovki-new-balance-998-art038',
          'item/870-krossovki-new-balance-998-art037',
          'item/868-krossovki-new-balance-998-art035',
          'item/867-krossovki-new-balance-998-art0034',
          'item/1110-krossovki-new-balance-998-art031',
          'item/1048-new-balance-999-art002',
          'item/1047-new-balance-999-art001',
          'item/1098-new-balance-999-art004',
          'item/1097-new-balance-999-art003',
          'item/1917-new-balance-999-art020',
          'item/1488-new-balance-580-art008',
          'item/1844-new-balance-999-art19',
          'item/1843-new-balance-999-art18-krasnyjj-red',
          'item/1842-new-balance-999-art17-seryjjbordovyjj-greywine-red',
          'item/1841-new-balance-999-art16-chernyjj-black',
          'item/1839-new-balance-999-art14-chernyjj-black',
          'item/1603-new-balance-999-art013',
          'item/1602-new-balance-999-art012',
          'item/1601-new-balance-999-art011',
          'item/1354-new-balance-999-art009',
          'item/1353-new-balance-999-art008',
          'item/1352-new-balance-999-art007',
          'item/1108-new-balance-999-art006',
          'item/1107-new-balance-999-art005',
          'item/1971-new-balance-1400-art005-sinijj-blue',
          'item/1972-new-balance-1400-art006-zelenyjj-green',
          'item/1846-new-balance-1400-art4-sinijj-blue',
          'item/997-krossovki-new-balance-1400-chernyjj-black-art002',
          'item/996-krossovki-new-balance-1400-chernyjj-black-art001']
newbalance_links = addDomain(newbalance_links)

# OLD недописанныая функция
def getProductInfoFromcatalog():
	url = 'http://s.rwns.ru/catalog-train.html'
	from grab import Grab
	g = Grab(log_file='product.html')
	g.go(url)

	products = []
	product = {}
	names = []
	briefs = []
	oldprice = []
	pirce = []
	prices = []
	test = []
	result = []
	i = 0
	q = 0
	b = 0
	p = 0 

	# Находим Имя
	elements = g.doc.select('//div/div/div/div/div[@class="catalog w"]/div[@class="items fix"]/div[@class="item"]/h3/a')
	for elem in elements:
		text = elem.text().replace("Кроссовки", "")
		names.append(text)
		q +=1


	# Находим Бриф name
	elements = g.doc.select('//div/div/div/div/div[@class="catalog w"]/div[@class="items fix"]/div[@class="item"]/div[@class="brief text"]')
	for elem in elements:
		text = elem.text()
		briefs.append(text)
		b +=1



	elements= g.doc.select('//div[@class="oldprice"]')
	for elem in elements:
		oldprice.append(elem.number())
		p +=1


	# i = 0
	# while i < q-2:
	# 	i+=1
	# 	result.append ( names[i] + ' ' + briefs[i] + '; ' + str(oldprice[i])  )
		
	result  = {'names':q , 'briefes':b , 'oldprices': p}


	return result


# OLD Получаем весь текст продукта 
def getProductsText(url):
	from grab import Grab
	g = Grab(log_file='product.html')
	g.go(url)

	names = g.doc.select('//div/div/div/div/div[@class="catalog w"]/div[@class="items fix"]/div[@class="item"]')
	products = []

	for elem in names:
		text = elem.text
		products.append(text)
	return products


# OLD Получаем SRC всех картинок на странице продукта
def getProductImages(url):
	from grab import Grab
	g = Grab(log_file='productImages.html')
	g.go(url)

	product = g.doc.select('//div[@class="product w item"]/div[@class="L"]/div[@class="album"]/a/img')
	if len(product) > 0:
		images_list = []
		for image in product:
		    src = image.attr('src')
		    src = fixImageUrl(src)
		    images_list.append(src)
		images_str = ', '.join(images_list)
	
	else:
		product2 = g.doc.select('//div[@class="product w item"]/div[@class="L"]/div/a/img')
		images_str = product2.attr('src')
		images_str = fixImageUrl(images_str)
	
	return images_str
