# Introduction 
	Python script to search for missing CareEvolve orders in StarLims

# Getting Started
	To run this script using Python
	Open a terminal and type the command > Python MissingCEOrders.py
		a file dialog will allow the user to select the HL7Ordermmddyy.xlsx file
		If no file is selected from the first file dialog box that the script will use the sync database
		a file dialog will allow the user to select the CEOrdermmddyy.xls file
		missing orders will be displayed on the output GUI screen
				
# Build and Test
	To make this script into an exe for windows
	Open a terminal windows
		Enter the command "pip install pyInstaller" if not already installed
		You may also need to install PyWin32 package
		Enter the command "pyInstaller --onefile MissingCEOrders.py"
		This will create all the necessary data and generate the script into an exe
		into a folder "dist"
		Zip this folder and provide to users to extract.
		they can extract into a folder to run from

# Contribute
	anyone can make changes just ensure it works
