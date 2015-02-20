import urllib
import urllib2
import json
import sublime, sublime_plugin

class HtmlToSlimFromSelectionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			if not region.empty():
				html = self.view.substr(region)
				slim = HTHTools.post_html_return_slim(html)
				if slim != None:
					self.view.replace(edit, region, slim)

	def is_enabled(self):
		return True #return self.view.file_name().endswith(".slim")

class HTHTools:
	@classmethod
	def post_html_return_slim(self, html):
		url = 'http://html2slim.raving.systems/html2slim.json'
		data_json = {'source' : html }
		data_json = data.encode('utf-8')
		data = urllib.urlencode(data_json)
		req = urllib2.Request(url, data_json)
		response = urllib2.urlopen(req)
		result = json.loads(response.read().decode("utf-8"))

		if result['result']:
			return result['result']
		else:
			return None
