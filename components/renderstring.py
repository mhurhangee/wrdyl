#Render String using textual's inbuilt functions
from textual.app import RenderResult
from textual.widget import Widget

class RenderString(Widget):
	def render(self, string) -> RenderResult:
		return string