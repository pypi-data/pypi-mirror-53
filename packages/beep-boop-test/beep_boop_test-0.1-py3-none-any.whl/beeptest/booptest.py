def beep(number=1):
	res = ""
	for i in range(number):
		if (i+1) % 2:
			res += "boop "
		else:
			res += "beep "
	print(res)

if __name__ == "__main__":
	a = input("Beep?")
	try:
		beep(int(a))
	except:
		print("Boop :(")