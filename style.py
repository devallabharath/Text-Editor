import wx
import wx.stc as stc

def style(self):
	self.control = stc.StyledTextCtrl(self)
	layout = wx.BoxSizer(wx.HORIZONTAL)
	layout.Add(self.control, proportion=1, border=0, flag=wx.ALL|wx.EXPAND)
	self.SetSizer(layout)
	self.control.SetWindowStyle(self.control.GetWindowStyle() | wx.DOUBLE_BORDER)
	self.control.SetMarginWidth(1, 18)
	self.font=self.cfg.get('settings','Fontface')
	self.cfont=self.cfg.get('settings','CFontface')
	self.fontsize=self.cfg.get('settings','Fontsize')
	self.cfontsize=self.cfg.get('settings','CFontsize')
	self.cstyle=self.cfg.get('settings','CStyle')
	self.control.StyleSetSpec(stc.STC_STYLE_DEFAULT, "back:#212121,face:"+self.font+ ",size:"+ self.cfontsize)
	self.control.StyleSetSpec(stc.STC_STYLE_LINENUMBER,  "fore:#BDBDBD,back:#212121,face:"+self.font+",size:"+self.cfontsize)
	self.control.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "fore:#FFFFFF,face:"+self.font)
	self.control.StyleSetSpec(stc.STC_H_DEFAULT, "fore:#ffffff,back:#212121,face:"+self.font+",size:"+self.fontsize)
	self.control.StyleSetSpec(stc.STC_STYLE_INDENTGUIDE, "fore:"+self.cfg.get('settings','GuideColor')+",back:#212121")
	self.control.StyleSetSpec(stc.STC_STYLE_BRACELIGHT, "fore:#0FF,back:#212121,bold")
	self.control.StyleSetSpec(stc.STC_STYLE_BRACEBAD, "fore:#fff,back:#212121,bold")
	self.control.SetUseAntiAliasing(self.cfg.getboolean('settings','Antialias'))
	self.control.SetBufferedDraw(self.cfg.getboolean('settings','BufferedDraw'))
	self.control.SetWrapIndentMode(2)
	self.control.SetWrapVisualFlags(2)
	self.control.SetCaretStyle(self.cfg.getint('settings','CaretStyle'))
	self.control.SetCaretWidth(self.cfg.getint('settings','CaretWidth'))
	self.control.SetCaretLineVisible(True)
	self.control.SetCaretForeground(self.cfg.get('settings','CaretColor'))
	self.control.SetCaretLineBackground(self.cfg.get('settings','LineHicolor'))
	self.control.SetCaretLineBackAlpha(self.cfg.getint('settings','LineHicoloralpha'))
	self.control.SetSelBackground(True,self.cfg.get('settings','SelBack'))
	self.control.SetSelAlpha(self.cfg.getint('settings','SelAlpha'))
	self.control.SetAdditionalSelectionTyping(True)
	self.control.SetMultipleSelection(self.cfg.getboolean('settings','MultiSelect'))
	self.control.SetMultiPaste(self.cfg.getboolean('settings','MultiPaste'))
	self.control.SetUseTabs(self.cfg.getboolean('settings','UseTabs'))
	self.control.SetEdgeMode(3)
	self.control.SetEdgeColumn(89)
	self.control.SetEdgeColour('#aaaaaa')
	# self.control.SetTabDrawMode(3)
	self.control.SetIndentationGuides(self.cfg.getboolean('settings','IndentGuides'))
	self.control.SetTabWidth(self.cfg.getint('settings','Tabwidth'))
	self.control.SetViewWhiteSpace(self.cfg.getboolean('settings','ShowWhitespaces'))
	self.control.SetWhitespaceSize(self.cfg.getint('settings','WhitespaceSize'))
	self.foldSymbols = 2

	if self.foldSymbols == 0:
		# Arrow pointing right for contracted folders, arrow pointing down for expanded
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_ARROWDOWN, "black", "black")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_ARROW, "black", "black")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_EMPTY, "black", "black")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_EMPTY, "black", "black")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_EMPTY, "white", "black")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, "white", "black")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, "white", "black")

	elif self.foldSymbols == 1:
		# Plus for contracted folders, minus for expanded
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_MINUS, "white", "black")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_PLUS,  "white", "black")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_EMPTY, "white", "black")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_EMPTY, "white", "black")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_EMPTY, "white", "black")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, "white", "black")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, "white", "black")

	elif self.foldSymbols == 2:
		# Like a flattened tree control using circular headers and curved joins
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_CIRCLEMINUS,          "white", "#404040")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_CIRCLEPLUS,           "white", "#404040")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,                "white", "#404040")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNERCURVE,         "white", "#404040")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_CIRCLEPLUSCONNECTED,  "white", "#404040")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_CIRCLEMINUSCONNECTED, "white", "#404040")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNERCURVE,         "white", "#404040")

	elif self.foldSymbols == 3:
		# Like a flattened tree control using square headers
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_BOXMINUS,          "white", "#808080")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_BOXPLUS,           "white", "#808080")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,             "white", "#808080")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNER,           "white", "#808080")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_BOXPLUSCONNECTED,  "white", "#808080")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, "white", "#808080")
		self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER,           "white", "#808080")

	# self.control.SetMarginBackground(2,'RED')
	# self.control.SetFoldMarginColour(True,'#000000')
	# self.control.BraceBadLightIndicator(True,2)
	# self.control.BraceBadLight(1)
	# self.control.BraceHighlightIndicator(True,1)
	# self.control.BraceHighlight(5,8)

	self.control.Bind(stc.EVT_STC_MODIFIED, self.refresh)
