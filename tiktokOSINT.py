#! /usr/bin/env python3
# TikTok OSINT Tool
# @author https://github.com/sc1341
# 
# The creator nor any contributors are responsible for any illicit
# use of this program
#
#
import argparse
import json
import os
import random
import requests
import sys

from banner import banner
from bs4 import BeautifulSoup
from useragents import *


class TikTokOSINT:

	def __init__(self, username):
		# Make sure that the usernames starts with @ for the http request
		if username.startswith('@'):
			self.username = username
		else:
			self.username = f'@{username}'
		
		self.create_dir()
		# Scrapes the profile and creates the data and posts objects
		self.data, self.posts = self.scrape_profile()
		# Save the data into the text file in the dir
		self.save_data()
		self.print_data()


	def scrape_profile(self):
		"""
		Scrapes the user profile and creates the data object
		which contains the user information
		:params: none
		:return:none
		"""
		r = requests.get(f'http://tiktok.com/{self.username}', headers={'User-Agent':random.choice(user_agents)})
		soup = BeautifulSoup(r.text,'html.parser')
		attrs = soup.find_all('meta')
		meta1 = soup.find_all('script')
		attrs = soup.find_all('meta')
		try:
			# content1 = attrs[27].get('content').split(',')
			# We know that it is 13 we are looking for... Now we need to figure out why it won't load
			#print(meta1[12].get_text())
			# Need to clean up what is going on with the splicing of content -- figured out hte main issue
			content1 = attrs[4].get('content').split('.')
			meta1 = json.loads(meta1[13].get_text())
			print(meta1)
			profiledata = {"username":self.username,
			'followers':content1[0],
			'following':content1[1],
			'bio':content1[6],
			'profilepictureurl':attrs[13].get('content'),
			'isVerified':meta1['/@:uniqueId']['userData']['verified'],
			'fans':meta1['/@:uniqueId']['userData']['fans'],
			'videos':meta1['/@:uniqueId']['userData']['video'],
			'userID':meta1['/@:uniqueId']['userData']['userId'],
			'nickname':meta1['/@:uniqueId']['userData']['nickName'],
			'likes':meta1['/@:uniqueId']['userData']['heart']}
			posts = meta1['/@:uniqueId']['itemList']
		except IndexError:
			print("Error: Profile Does not exist!")
			sys.exit()
		return profiledata, posts

	def download_profile_picture(self):
		"""Downloads the profile picture
		:params: none
		:return: none
		"""
		r = requests.get(self.data['profilepictureurl'])
		with open(f"{self.username}.jpg","wb") as f:
			f.write(r.content)

	def save_data(self):
		"""
		Dumps the dict into a json file in the user directory
		:params: none
		:return: none
		"""
		with open(f'{self.username}_profile_data.json','w') as f:
			f.write(json.dumps(self.data))
		with open(f'{self.username}_post_data.json', 'w') as f:
			f.write(json.dumps(self.posts))
		print(f"Profile and Post data saved to {os.getcwd()}")


	def create_dir(self):
		"""
		Create a directory to put all of the OSINT files into,
		it also avoid a possible error with a directory already existing
		:params: none
		:return: none
		"""
		i = 0
		while True:
			try:
				os.mkdir(self.username + str(i))
				os.chdir(self.username + str(i))
				break
			except FileExistsError:
				i += 1

	def print_data(self):
		"""Prints out the data to the cmd line
		:params:none
		:return: none
		"""
		for key, value in self.data.items():
			print(f"{key.upper()}: {value}")


def arg_parse():
	parser = argparse.ArgumentParser(description="TikTok OSINT Tool")
	parser.add_argument("--username", help="Profile Username", required=True, nargs=1)
	parser.add_argument("--downloadProfilePic", help="Downloads the user profile picture", required=False, action='store_true')
	return parser.parse_args()

def main():
	print(banner)
	args = arg_parse()
	if args.downloadProfilePic == True:
		tiktok = TikTokOSINT(args.username[0])
		tiktok.download_profile_picture()
	else:
		tiktok = TikTokOSINT(args.username[0])


if __name__ == "__main__":
	main()
