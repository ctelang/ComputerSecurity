import  sys, urllib, urllib.parse
from pymd5 import md5, padding


url = sys.argv[1]
firstToken = url[:url.find("=") + 1]
orgToken = url[url.find("=") + 1:url.find("&")]
urlMessage = url[url.find("&") + 1:]
messageLength = (len(urlMessage) + 8)
finalBits = (messageLength + len(padding(messageLength *8))) * 8
h = md5(state=bytes.fromhex(orgToken), count=finalBits)
safeUnlock = "&command=UnlockSafes"
h.update(safeUnlock)
finalToken = h.hexdigest()
new_url = firstToken + finalToken + "&" + urlMessage + urllib.parse.quote(padding(messageLength*8)) + safeUnlock
print(new_url)