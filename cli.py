from phext import PhextSearcher
from PIL import Image


searcher = PhextSearcher()
searcher.fit()
while True:
	query = input("Enter a description to search your gallery: ")
	if query == 'exit':
		break
	best_fit, _ = searcher.search(query)

	img = Image.open(f'images/{best_fit}')
	img.show()
