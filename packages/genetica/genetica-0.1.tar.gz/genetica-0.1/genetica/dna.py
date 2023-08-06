# -*- coding: utf-8 -*-
"""DNA module

	Logics of the DNA chains manipulation and creation
"""


import random


class DNA:
	def __init__(self, genes_num):

		# Create a random genes set
		self.genes = [round(random.uniform(0, 1), 2) for i in range(genes_num)]

	def mutate(self, mutation_prob):
		"""
		Apply the mutation to the genes set
		:param mutation_prob: probability of mutation
		"""

		for i in range(len(self.genes)):
			if random.uniform(0, 1) > mutation_prob:
				continue

			self.genes[i] = round(random.uniform(0, 1), 2)


def genify(options_list, gen):
	"""
	Choose position from interval of discrete parameters based on gen value
	:param options_list: List of discrete values
	:param gen: DNA gen value
	:return:
	"""

	# Probability steps for projecting to given gen
	prob_step = round(1 / len(options_list), 2)

	for i in range(len(options_list)):
		if gen <= i * prob_step:
			return options_list[i]
