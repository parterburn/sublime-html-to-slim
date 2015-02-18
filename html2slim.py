import urllib.request
import json
import sublime, sublime_plugin

settings = sublime.load_settings("html2slim.sublime-settings")

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
		host = 'http://html2slim-json.herokuapp.com/api.json'
		attributes_style = settings.get("attributes_style", "default")
		data = { 'page': {'html': html}, 'options': {attributes_style: 'true'} }
		data_json = json.dumps(data)
		data_json = data_json.encode('utf-8')
		req = urllib.request.Request(host, data_json, {'content-type': 'application/json'})
		response_stream = urllib.request.urlopen(req)
		result = json.loads(response_stream.read().decode("utf-8"))

		if result["page"]:
			return result["page"]["slim"]
		else:
			return None
