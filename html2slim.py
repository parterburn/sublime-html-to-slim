import urllib.request
import urllib2
import json
import sublime, sublime_plugin

class HtmlToSlimFromFileCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		source = self.view.file_name()
		if source.endswith(".erb"):
			target = source.replace('.erb', '.slim')
		if source.endswith(".html"):
			target = source + '.slim'
		if target:
			with open(source, 'r') as f:
				html = f.read()
			slim = HTHTools.post_html_return_slim(html)
			if slim != None:
				with open(target, 'w') as f:
					f.write(slim)
				self.view.window().open_file(target)

	def is_enabled(self):
		return True #return (self.view.file_name().endswith(".html") or self.view.file_name().endswith(".erb"))

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

class HtmlToSlimFromOtherSelectionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			if not region.empty():
				html = self.view.substr(region)
				slim = HTHTools.post_html_return_slim_other(html)
				if slim != None:
					self.view.replace(edit, region, slim)

	def is_enabled(self):
		return True #return self.view.file_name().endswith(".slim")		

class HtmlToSlimFromClipboardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		html = sublime.get_clipboard()
		slim = HTHTools.post_html_return_slim(html)
		if slim != None:
			for region in self.view.sel():
				self.view.replace(edit, region, slim)

	def is_enabled(self):
		return True #return self.view.file_name().endswith(".slim")

class HTHTools:
	@classmethod
	def post_html_return_slim(self, html):
		host = 'http://html2slim.raving.systems/html2slim.json'
		data = { 'source' : html }
		data_json = json.dumps(data)
		data_json = data_json.encode('utf-8')
		req = urllib.request.Request(host, data_json, {'content-type': 'application/json'})
		response_stream = urllib.request.urlopen(req)
		result = json.loads(response_stream.read().decode("utf-8"))

		if result["result"]:
			return result["result"]
		else:
			return None

	def post_html_return_slim_other(self, html):
		url = 'http://html2slim.raving.systems/html2slim.json'
		data = { 'source' : html }
		data_json = data.encode('utf-8')
		data_json = urllib.urlencode(data_json)
		req = urllib2.Request(url, data_json)
		response = urllib2.urlopen(req)
		result = json.loads(response.read().decode("utf-8"))

		if result['result']:
			return result['result']
		else:
			return None