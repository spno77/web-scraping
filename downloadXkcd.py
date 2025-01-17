#! python3
# downloadXkcd.py -- Downloads every single XKCD comic

import requests, os, bs4

url = 'http://xkcd.com'
os.makedirs('xkcd',exist_ok=True)

while not url.endswith('#'):
	print('Downloading page %s...' %url)
	res = requests.get(url)
	res.raise_for_status()

	soup = bs4.BeautifulSoup(res.text,"html.parser")

	#find the url of the comic page

	comicElem = soup.select('#comic img')
	if comicElem == []:
		print('could not find comic image.')
	else:
		comicUrl = comicElem[0].get('src').strip("http://")
		comicUrl = "http://" + comicUrl
		# Download the image
		print('Downloading image %s...' %(comicUrl))
		res = requests.get(comicUrl)
		res.raise_for_status()
		#save the image to ./xkcd
		imageFile = open(os.path.join('xkcd',os.path.basename(comicUrl)),'wb')
		for chunk in res.iter_content(100000):
			imageFile.write(chunk)
		imageFile.close()
	#get the previous button url
	prevLink = soup.select('a[rel="prev"]')[0]
	url = 'http://xkcd.com' + prevLink.get('href')

print('Done')


