from grab import Grab

url = 'yandex.ru'
log_file = 'out.html'
g = Grab(log_file=log_file)

g.go('http://moscross.ru/catalog/kedy-vans')




for elem in g.doc.select('//div/div/div/div/div[@class="catalog w"]/div[@class="items fix"]/div[@class="item"]'):
    print (elem.text())
