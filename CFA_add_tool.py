import os, sys, re, PIL.Image, Tkinter, tkFileDialog, tkMessageBox, ScrolledText
from Tkinter import *

#Globals
dir = ""
image = ""

# Dictionaries & Lists
fileToClan = {
  "Anger Feather.txt": "Angel Feather",
  "Aqua Force.txt": "Aqua Force",
  "Bermuda.txt": "Bermuda Triangle",
  "Cray Elemental.txt": "Cray Elemental",
  "Dark Irregulars.txt": "Dark Irregulars",
  "Dimension Police.txt": "Dimension Police",
  "Etrangers.txt": "Etranger",
  "Gear Chronicle.txt": "Gear Chronicle",
  "Genesis.txt": "Genesis",
  "Gold Paladin.txt": "Gold Paladin",
  "Granblue.txt": "Granblue",
  "Great Nature.txt": "Great Nature",
  "Kagero.txt": "Kagero",
  "Link Joker.txt": "Link Joker",
  "Megacolony.txt": "Megacolony",
  "Murakumo.txt": "Murakumo",
  "Narukami.txt": "Narukami",
  "Neo Nectar.txt": "Neo Nectar",
  "Nova Grappler.txt": "Nova Grappler",
  "Nubatama.txt": "Nubatama",
  "Oracle.txt": "Oracle Think Tank",
  "Order Cards.txt": "Order Card",
  "Pale Moon.txt": "Pale Moon",
  "Royal Paladin.txt": "Royal Paladin",
  "Shadow Paladin.txt": "Shadow Paladin",
  "Spike Brothers.txt": "Spike Brothers",
  "Tachikaze.txt": "Tachikaze",
  "The Mask Collection.txt": "The Mask Collection",
  "Touken Ranbu.txt": "Touken Ranbu"
}
# Easier to just flip the dictionary then make it two way
clanToFile = dict(map(reversed, fileToClan.items()))
clanNum = {
  "Angel Feather" : 16,
  "Aqua Force" : 3,
  "Bermuda Triangle" : 13,
  "Cray Elemental" : 25,
  "Dark Irregulars" : 11,
  "Dimension Police" : 6,
  "Etranger" : 22,
  "Gear Chronicle" : 26,
  "Genesis" : 21,
  "Gold Paladin" : 5,
  "Granblue" : 8,
  "Great Nature" : 7,
  "Kagero" : 12,
  "Link Joker" : 24,
  "Megacolony" : 2,
  "Murakumo" : 20,
  "Narukami" : 19,
  "Neo Nectar" : 9,
  "Nova Grappler" : 4,
  "Nubatama" : 23,
  "Oracle Think Tank" : 10,
  "Order Card" : 30,
  "Pale Moon" : 18,
  "Royal Paladin" : 15,
  "Shadow Paladin" : 1,
  "Spike Brothers" : 14,
  "Tachikaze" : 17,
  "The Mask Collection" : 28,
  "Touken Ranbu" : 27
}
grades = [0, 1, 2, 3, 4, 5]
gifts = {
	"None" : "", 
	"Accel" : "global.OrangeTokenAdd[CardStat] = 1", 
	"Force" : "global.BlueTokenAdd[CardStat] = 1", 
	"Protect" : "global.GreenTokenAdd[CardStat] = 1"
}
types = {
	"Normal Unit" : "", 
	"G Unit" : "global.ExtraDeck[CardStat] = 1", 
	"Draw Trigger" : "global.TriggerUnit[CardStat] = 1",
	"Critical Trigger" : "global.TriggerUnit[CardStat] = 2",  
	"Stand Trigger" : "global.TriggerUnit[CardStat] = 3",
	"Heal Trigger" : "global.TriggerUnit[CardStat] = 4",
	"Front Trigger" : "global.TriggerUnit[CardStat] = 5"
}

# Create and run UI
def main() :   
	window = Tkinter.Tk()
	window.title('CFA add tool')
	
	# On click events
	def clickDir():
		global dir
		dir = tkFileDialog.askdirectory()
		dirTextVar.set(dir)
		
		# Update options menu
		clanMenu = clanOptions['menu']
		clanMenu.delete(0, 'end')
		clanOptionVar.set("")
		clanOptions.configure(state="disabled")
		if (dir != "") :
			options = clanList()
			if (len(options) > 0) :
				clanOptionVar.set(options[0])
				clanOptions.configure(state='normal') 
				for clan in options:
					clanMenu.add_command(label=clan, command=lambda clan=clan: clanOptionVar.set(clan))
		
	def clickImage():
		global image
		image = tkFileDialog.askopenfilename(title = "Select image",filetypes = (("png","*.png*"),("jpeg","*.jpg")))
		imgTextVar.set(image)
		
	def clickSubmit():
		if (not dir) :
			tkMessageBox.showinfo("Error", "Please set directory")
		elif (not image) :
			tkMessageBox.showinfo("Error", "Please set image")
		elif (not nameEntryVar.get()) :
			tkMessageBox.showinfo("Error", "Name cannot be empty")
		elif (not powerEntryVar.get()) :
			tkMessageBox.showinfo("Error", "Power cannot be empty")
		elif (not clanOptionVar.get()) :
			tkMessageBox.showinfo("Error", "Please set clan")
		else :
			submit()
	
	# Min window size
	window.columnconfigure(8, weight=1)
	window.rowconfigure(15, weight=1)
	col_count, row_count = window.grid_size()
	for col in xrange(col_count):
		window.grid_columnconfigure(col, minsize=20)
	for row in xrange(row_count):
		window.grid_rowconfigure(row, minsize=20)
	
	# Filepaths
	Tkinter.Button(window, text = "Directory", command = clickDir).grid(row = 1, column = 1, sticky=W+E)	
	global dirTextVar
	dirTextVar = Tkinter.StringVar()
	dirTextVar.set(dir)
	dirTextEntry = Tkinter.Entry(window, textvariable = dirTextVar)
	dirTextEntry.configure(state="disabled")
	dirTextEntry.grid(row = 1, column = 3, sticky=W+E, columnspan=5)

	Tkinter.Button(window, text = "Image", command = clickImage).grid(row = 2, column = 1, sticky=W+E)
	global imgTextVar
	imgTextVar = Tkinter.StringVar()
	imgTextVar.set(image)
	imgTextEntry = Tkinter.Entry(window, textvariable = imgTextVar)
	imgTextEntry.configure(state="disabled")
	imgTextEntry.grid(row = 2, column = 3, sticky=W+E, columnspan=5)

	# Name / skill
	Tkinter.Label(window, text = "Name").grid(row = 4, column = 1, sticky=E)
	global nameEntryVar
	nameEntryVar = Tkinter.StringVar()
	Tkinter.Entry(window, textvariable = nameEntryVar).grid(row = 4, column = 3, sticky=W+E)

	Tkinter.Label(window, text = "Skill").grid(row = 5, column = 1, sticky=E)
	global skillText
	skillText = Tkinter.Text(window, wrap='word', width=30, height=10)
	skillText.grid(row = 4, column = 3, sticky=W+E, rowspan=8)

	# Card info		
	Tkinter.Label(window, text = "Power").grid(row = 4, column = 5, sticky=E)
	global powerEntryVar
	powerEntryVar = Tkinter.StringVar()
	Tkinter.Entry(window, textvariable = powerEntryVar, width=10).grid(row = 4, column = 7, sticky=W+E)
	
	Tkinter.Label(window, text = "Grade").grid(row = 5, column = 5, sticky=E)
	global gradeOptionVar
	gradeOptionVar = Tkinter.StringVar()
	gradeOptions = Tkinter.OptionMenu(window, gradeOptionVar, "", *"")
	gradeOptions.grid(row = 5, column = 7, sticky=W+E)
	gradeMenu = gradeOptions['menu']
	gradeMenu.delete(0, 'end')
	for grade in grades:
		gradeMenu.add_command(label=grade, command=lambda grade=grade: gradeOptionVar.set(grade))
	gradeOptionVar.set(grades[0])
	
	Tkinter.Label(window, text = "Clan").grid(row = 6, column = 5, sticky=E)
	global clanOptionVar
	clanOptionVar = Tkinter.StringVar()
	global clanOptions
	clanOptions = Tkinter.OptionMenu(window, clanOptionVar, "", *"")
	clanOptions.configure(state="disabled")
	clanOptions.grid(row = 6, column = 7, sticky=W+E)
	
	Tkinter.Label(window, text = "Race").grid(row = 7, column = 5, sticky=E)
	global raceEntryVar
	raceEntryVar = Tkinter.StringVar()
	Tkinter.Entry(window, textvariable = raceEntryVar).grid(row = 7, column = 7, sticky=W+E)
	
	Tkinter.Label(window, text = "Type").grid(row = 8, column = 5, sticky=E)
	global typeOptionVar
	typeOptionVar = Tkinter.StringVar()
	typeOptions = Tkinter.OptionMenu(window, typeOptionVar, "", *"")
	typeOptions.grid(row = 8, column = 7, sticky=W+E)
	typeMenu = typeOptions['menu']
	typeMenu.delete(0, 'end')
	for type in types.keys():
		typeMenu.add_command(label=type, command=lambda type=type: typeOptionVar.set(type))
	typeOptionVar.set("Normal Unit" )
	
	Tkinter.Label(window, text = "Gift").grid(row = 9, column = 5, sticky=E)
	global giftOptionVar
	giftOptionVar = Tkinter.StringVar()
	giftOptions = Tkinter.OptionMenu(window, giftOptionVar, "", *"")
	giftOptions.grid(row = 9, column = 7, sticky=W+E)
	giftMenu = giftOptions['menu']
	giftMenu.delete(0, 'end')
	for gift in gifts.keys():
		giftMenu.add_command(label=gift, command=lambda gift=gift: giftOptionVar.set(gift))
	giftOptionVar.set("None")

	#--
	
	global feedbackText
	feedbackText = Tkinter.Text(window, wrap='word', width=5, height=5, bg="light grey")
	feedbackText.grid(row = 12, column = 1, sticky=W+E, rowspan=3, columnspan=5)
	feedbackText.configure(state="disabled")
	
	# Create
	Tkinter.Button(window, text = "Create", command = clickSubmit).grid(row = 12, column = 7, sticky=W+E, rowspan=3)
		
	#window.geometry("400x200")
	window.mainloop()
	
	return


def submit() : 
	# Total card number
	cardNum = updateNum()
	if (cardNum == -1) : 
		report("Error reading/writing to file %s/Text/NoUse.txt" % (dir))
		return
	report("File %s/Text/NoUse.txt updated. New card num is %d." % (dir, cardNum))
	
	# Card sprites
	if (resize(300, 437, '%s/n%d' % ("%s/CardSprite" % (dir), cardNum)) == -1) :
		report("Error creating image %s/CardSprite/%d" % (dir, cardNum))
		return
	if (resize(60, 87, '%s/n%d' % ("%s/CardSpriteMini" % (dir), cardNum)) == -1) :
		report("Error creating image %s/CardSpriteMini1/%d" % (dir, cardNum))
		return
	if (resize(75, 109, '%s/n%d' % ("%s/CardSpriteMini2" % (dir), cardNum)) == -1) :
		report("Error creating image %s/CardSpriteMini2/%d" % (dir, cardNum))
		return
	
	if (updateClan(cardNum) == -1) :
		report("Error updating " % (dir))
		return
	
	report("Finished successfully")
	#os.system("notepad.exe %s/Text/%s" % (dir, clanToFile[clanOptionVar.get()]))
	
	return
	
def report(msg) :
	feedbackText.configure(state="normal")
	feedbackText.insert(END,"\n%s\n" % msg)
	feedbackText.configure(state="disabled")
	return	
	
# Add 1 to current card count (global.AllCard) in .../Text/NoUse.txt. Returns the new count, -1 on error.
def updateNum() :
	data = ""
	
	#read
	try :
		with open('%s/Text/NoUse.txt' % (dir), 'r') as file:
			data = file.read()
			file.close()
	except IOError :
		return -1
	
	#replace line
	oldLine = re.findall('AllCard = .+', data)[0]
	newVal = int(oldLine.replace("AllCard = ", "")) + 1
	newLine = "AllCard = %d" % newVal
	data = data.replace(oldLine, newLine)

	#write
	try :
		with open('%s/Text/NoUse.txt' % (dir), 'w') as file:
			file.write(data)
			file.close()
	except IOError :
		return -1
	
	return newVal
	
# Open image, resize and save with new name. Returns 0, -1 on error.
def resize(xSize, ySize, saveName) : 
	try:
		im = PIL.Image.open(image)
		im = im.resize((xSize,ySize), PIL.Image.ANTIALIAS)
		im = im.convert('RGB')
		im.save('%s.jpg' % saveName) 
	except IOError:
		return -1
				
	report('Saved file %s.jpg' % saveName)
	return 0

# Get list of clans with files in .../Text/
def clanList() :
	list = []
	for file in os.listdir("%s/Text" % dir) :
		if str(file) in fileToClan :
			list.append(fileToClan[str(file)])
			
	return list
	

def updateClan(cardNum) :
	#append
	try :
		with open('%s/Text/%s' % (dir, clanToFile[clanOptionVar.get()]), 'a') as file:
			file.write(getCard(cardNum))
			file.close()
	except IOError :
		return -1	
		
	return 0
	
# Create string to represent card in clan file
def getCard(cardNum) :
	card = ""
	cardStat = "\nCardStat = %d" % cardNum
	name = "global.CardName[CardStat] = '%s'" %  nameEntryVar.get()
	text = "global.CardText[CardStat] ='%s/%s\n\n%s'" % (clanOptionVar.get(), raceEntryVar.get(), skillText.get("1.0",END))
	grade = "global.UnitGrade[CardStat] = %s" % gradeOptionVar.get()
	clanNumber = "global.CardInClan[CardStat] = %s" % clanNum[clanOptionVar.get()]
	gift = gifts[giftOptionVar.get()]
	if (gift != "") : gift = gift = "\n"
	type = types[typeOptionVar.get()]
	if (type != "") : type = type = "\n"
	power = "global.PowerStat[CardStat] = %s" % powerEntryVar.get()
	
	# G Unit type before bracket }, all other types after
	if (typeOptionVar.get() == "G Unit") :
		card = "\n%s\n{\n%s\n%s\n%s\n%s\n%s}\n%s%s" % (cardStat, name, text, grade, clanNumber, type, gift, power)
	else :
		card = "\n%s\n{\n%s\n%s\n%s\n%s\n}\n%s%s%s" % (cardStat, name, text, grade, clanNumber, type, gift, power)
	
	return card
	
main()