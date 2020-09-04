import os, polib

po = polib.pofile(os.path.join(".","hu.po"), encoding='iso-8859-1')

po_out = polib.POFile(encoding='iso-8859-1')


po_out.metadata = {
    'Project-Id-Version': '1.0',
    'Report-Msgid-Bugs-To': 'you@example.com',
    'POT-Creation-Date': '2007-10-18 14:00+0100',
    'PO-Revision-Date': '2007-10-18 14:00+0100',
    'Last-Translator': 'you <you@example.com>',
    'Language-Team': 'English <yourteam@example.com>',
    'MIME-Version': '1.0',
    'Content-Type': 'text/plain; charset=utf8',
    'Content-Transfer-Encoding': 'iso-8859-1',
}


for entry in po:
	newEntry=polib.POEntry()
	if entry.msgid_plural != "":
		newEntry.msgid=entry.msgid+entry.msgid_plural
		newEntry.msgstr=entry.msgstr_plural[u'0']+entry.msgstr_plural[u'1']
	else:
		newEntry = entry
	po_out.append(newEntry)
	
po_out.save("hu2.po")
		
	


