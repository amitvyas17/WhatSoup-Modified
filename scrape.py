from main import locate_chat, scroll_to_top, run_scrap_group, to_sqlite

def main():
	locate_chat("Mama Jio") # Type here the name to scrap
	scroll_to_top() 
	run_scrap_group() # Run the scraper and save to csv file

	# Now if you wanna save it to a sqlite database table
	to_sqlite()

if __name__ == '__main__':
	main()