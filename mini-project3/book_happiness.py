"""This program determines the sentiment of books with reference to the year in which they were published.  
Essentially, it will show how happy people were in a given year.
The Gutenberg book needs to include the published date early in the text for this program to work."""
import pattern
import string
from pattern.web import *
from pattern.en import sentiment
from pattern.en import positive
import matplotlib.pyplot as plt
import os, sys
import numpy as np
import pickle

# Save data to a file (will be part of your data fetching script)


def get_files(path):
	"""Creates a list of txt files from the given directory.
	path: string that corresponds to directory"""
	book_list = []
	dirs = os.listdir(path)
	for text in dirs:
		if text != '.DS_Store':
			text = path + '/' + text
			book_list.append(text)
	return book_list


def get_word_list(file_name):
	""" Reads the specified project Gutenberg book.  Header comments and
		punctuation, are stripped away. Returns a lowercase string of the book.
		filename: any plain text file (.txt)
	"""
	f = open(file_name,'r')
	lines = f.readlines()
	curr_line = 0
	while lines[curr_line].find('START OF THIS PROJECT GUTENBERG EBOOK') == -1:
		curr_line += 1
	lines = lines[curr_line+1:]
	punct = string.punctuation

	no_punct = ""
	for line_current in lines:
		for element in line_current:
			if element not in punct:
				no_punct = no_punct + element
	return no_punct.lower()

def get_sentimentality(file_name):
	"""Reads the specifed Gutenberg book (without punctuation, headers, or uppercase letters) and returns 
	the sentiment in the form of a tuple (polarity, subjectivity).
	filename: any plain text file (.txt)
	"""
	book = get_word_list(file_name)
	return sentiment(book)

def list_book(file_name):
	"""The function returns a list of the words used in the book as a list.
		All words are converted to lower case."""
	no_punct = get_word_list(file_name)
	book_final = no_punct.split()
	return book_final

def publish_year(file_name):
	"""Searches through the specifed file to find the first year in the text.  It is assumed that the
	first year that shows up is the year the Gutenberg book was published
	filename: any plain text file (.txt)"""
	book = list_book(file_name)
	four_list = []
	for word in book:
		if len(word)==4:
			four_list.append(word)

	date_list = []

	numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	for word in four_list:
		for letter in range(4):
			if word[letter] in numbers:
				date_list.append(word)

	year_publish = date_list[0]
	return year_publish

def make_dictionary(file_list):
	"""Creates a dictionary with the keys from a list of book files and the values the publishing year
	and sentiment of the book
	file_list = list of string that correspond to .txt files"""
	names_years = {}
	for i in range(len(file_list)):
		names_years[file_list[i]] = (publish_year(file_list[i]), get_sentimentality(file_list[i]))
	return names_years

def make_plot(file_list):
	"""Using a dictionary, plots a book's relative happiness in reference to the year it was published.
	Input is a list of txt files generated by the get_file function.
	file_list = list of string that correspond to .txt files"""
	D = make_dictionary(file_list)
	for book in file_list:
		plt.plot(D.get(book)[0:1], D.get(book)[1][0]*100,'o-')
	

	plt.xlabel('year published')
	plt.ylabel('relative happiness')
	plt.title('Relative Happiness Over Years Based on Most Popular 30 Books In Gutenberg Project', fontsize=18)
	plt.show()


book_list = get_files('books')
make_plot(book_list)
