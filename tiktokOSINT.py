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
		if username.startswith('@qtr.aa'):
			self.username = @qtraa
		else:
			self.username = f'@{qtr.aa}'
		
		self.create_dir()
		# Scrapes the profile and creates the data and posts objects
		self.data = self.scrape_profile()
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
		r = requests.get(f'https://tiktok.com/{self.username}', headers={'User-Agent':random.choice(user_agents)})
		soup = BeautifulSoup(r.text, "html.parser")

		content = soup.find_all("script", attrs={"type":"application/json", "crossorigin":"anonymous"})

		content = json.loads(content[0].contents[0])

		print(content["props"]["pageProps"])

		profile_data = {
			"UserID":content["props"]["pageProps"]["userInfo"]["user"]["id"],
			"username":content["props"]["pageProps"]["userInfo"]["user"]["uniqueId"],
			"nickName":content["props"]["pageProps"]["userInfo"]["user"]["nickname"],
			"bio":content["props"]["pageProps"]["userInfo"]["user"]["signature"],
			"profileImage":content["props"]["pageProps"]["userInfo"]["user"]["avatarLarger"],
			"following":content["props"]["pageProps"]["userInfo"]["stats"]["followingCount"],
			"followers":content["props"]["pageProps"]["userInfo"]["stats"]["followerCount"],
			"fans":content["props"]["pageProps"]["userInfo"]["stats"]["followerCount"],
			"hearts":content["props"]["pageProps"]["userInfo"]["stats"]["heart"],
			"videos":content["props"]["pageProps"]["userInfo"]["stats"]["videoCount"],
			"verified":content["props"]["pageProps"]["userInfo"]["user"]["verified"]
			}

		return profile_data

	def download_profile_picture(self):
		"""Downloads the profile picture
		:params: none
		:return: none
		"""
		r = requests.get(self.data['profileImage'])
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
		#with open(f'{self.username}_post_data.json', 'w') as f:
			#f.write(json.dumps(self.posts))
		print(f"Profile data saved to {os.getcwd()}")


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
				os.mkdir(self.username)
				os.chdir(self.username)
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
