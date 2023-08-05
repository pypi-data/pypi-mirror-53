import requests
import os,json,random
from fake_useragent import UserAgent
class session(object):
	def __init__(self,username,password):

		

		self.api_test="https://api.myip.com"
		self.countries=["al", "ar", "am", "au", "at", "az", "bd", "by", "be", "bo", "br",
			"bg", "kh", "ca", "cl", "cn", "co", "cy", "cz", "dk", "do", "ec", "eg",
			"ee", "fi", "fr", "ge", "de", "gr", "gt", "hk", "hu", "is", "in", "id",
			"ie", "il", "it", "jm", "jp", "jo", "kz", "kr", "kg", "la", "lv", "lt",
			"lu", "my", "mx", "md", "ma", "nl", "nz", "no", "pk", "pa", "pe", "ph",
			"pl", "pt", "ro", "ru", "sa", "sg", "sk", "za", "es", "lk", "se", "ch",
			"tw", "tj", "th", "tr", "tm", "ua", "ae", "gb", "us", "uz", "vn"]
		self.cc=True


		self.username=username
		self.password=password
		self.timeout=None
		self.port = 22225
		self.dynamic=True
		self.host="zproxy.lum-superproxy.io"
		self.headers={"User-Agent": UserAgent().random}
		return None
	def generate_proxies(self,**kwargs):
		if "cc" in kwargs:
			cc=kwargs["cc"]
		else:
			cc=self.cc


		if type(cc)==bool:
			_country_code="-country-{}".format(random.choice(self.countries)) if cc else ""
		else:
			_country_code="-country-{}".format(cc[:2].lower())

		res={}
		for schema in ["http","https"]:
			res[schema]="{schema}://{username}{route}{country_code}:{password}@{host}:{port}".format(schema=schema,username=self.username,
			route="-route_err-pass_dyn" if self.dynamic else "-route_err-block",
			country_code=_country_code, password=self.password,port=self.port,host=self.host
			)

		return res
	def get(self,url,method='get', **kwargs):


		session=requests.session()
		session.proxies=self.generate_proxies(**kwargs)
		configable={"headers":self.headers,"timeout":self.timeout}
		params=kwargs
		for k,v in configable.items():
			if not k in params:
				params[k]=v
		if "cc" in kwargs:
			del(kwargs["cc"])

		if method.lower()=="post":
			method=session.post
		else:
			method=session.get
		return method(url,**params)
	def post(self,*args,**kwargs):
		return self.get(method="post",*args,**kwargs)
	def test(self,**kwargs):
		return self.get(self.api_test,**kwargs).json()

if __name__=="__main__":
	sess=session("{username}","{password}")
	print(sess.test())
