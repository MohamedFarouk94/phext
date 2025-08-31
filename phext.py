from embedding import create_embeddings
from search import search


class PhextSearcher:
	def __init__(self, path='images'):
		self.path = path

	def fit(self):
		create_embeddings(image_folder=self.path)

	def search(self, query, N=5):
		return search(query, N=N)
