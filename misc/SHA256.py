import hashlib
import base64
import sys

# calcul le hash d'un fichier et le stock en format BASE64 dans un fichier .ba

if len(sys.argv) < 1:
	print "Usage fichierAHasher"
else:
	inputFile = sys.argv[1]
	openedFile = open(inputFile)
	readFile = openedFile.read()

	sha256Hash = hashlib.sha256(readFile)
	sha256Hashed = sha256Hash.hexdigest()

	sha256HashedUp = sha256Hashed.upper()

	sha256Hashedb64 = base64.b64encode(sha256HashedUp)

	print "Hashing file: " + inputFile + ", result: " + sha256Hashedb64
	
	if inputFile[-4:] == ".exe":
		outputFile = inputFile[:-4] + '.ba'
	else:
		outputFile = inputFile + '.ba'
	

	openedOuputFile = open(outputFile,'w')
	openedOuputFile.write(sha256Hashedb64)
	openedOuputFile.close()
