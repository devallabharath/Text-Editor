import os
import wx
import wx.stc as stc
import configparser

class win(wx.Frame):

	def __init__(self, *args, **kwargs):
		super(win, self).__init__(*args, **kwargs)
		self.Show()
		self.SetIcon(wx.Icon("icons/icon.ico"))
		self.SetSize(1000,600)
#		self.Move(90,50)
		self.Center()
		# self.Maximize(True)
		# self.ShowFullScreen(True)

		self.cfg = configparser.RawConfigParser()
		self.cfg.read('style.cfg')
		self.par=dict(self.cfg.items("settings"))
		for p in self.par:
		    self.par[p]=self.par[p].split("#",1)[0].strip()

		globals().update(self.par)

		self.statusbar=self.CreateStatusBar(3)
		self.statusbar.SetStatusWidths([-1,-4,-1])
		self.statusbar.SetBackgroundColour('#BDBDBD')
		self.statusbar.SetForegroundColour('#FFFFFF')
		self.timer=wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.statlineinfo)
		self.timer.Start(40)
		self.Bind(wx.EVT_CLOSE, self.close)
		self.Menu()
		self.style()
		self.init()

	def filetype(self):
		if self.filepath=='untitled':
			pass
		else:
			dirs = os.path.dirname(self.filepath)
			basename = os.path.basename(self.filepath)
			info = os.path.splitext(basename)
			self.name = info[0]
			self.fileext = info[1]

	def title(self):
		self.filetype()
		if self.fileext=='.cfg':
			if self.name=='keybinds':
				self.SetTitle("Dev-Pad -- [KEYBINDS]" )
			elif self.name=='style':
				self.SetTitle("Dev-Pad -- [SETTINGS]")
			else:
				self.SetTitle("Dev-Pad -- %s" % self.filepath)
		else:
			self.SetTitle("Dev-Pad -- %s" % self.filepath)

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

	def syntax(self):
		if self.filepath=='untitled':
			pass
		elif self.fileext=='.cfg':
			self.control.SetLexer(stc.STC_LEX_PYTHON)
			self.control.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:#616161,back:#212121,"+self.cstyle+",face:"+self.cfont+",size:"+self.cfontsize)
			self.control.StyleSetSpec(stc.STC_P_OPERATOR, "fore:white,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#80DEEA,back:#212121,face:"+self.font+",size:"+self.fontsize)
		elif self.fileext=='.css':
			self.control.SetLexer(stc.STC_LEX_CSS)
			self.control.StyleSetSpec(stc.STC_CSS_DEFAULT, "fore:white,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_CSS_COMMENT, "fore:#616161,back:#212121,"+self.cstyle+",face:"+self.cfont+",size:"+self.cfontsize)
			self.control.StyleSetSpec(stc.STC_CSS_ID, "fore:#D81B60,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_CSS_TAG, "fore:#9CCC65,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_CSS_CLASS, "fore:#D81B60,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_CSS_VALUE, "fore:#7E57C2,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_CSS_OPERATOR, "fore:#ffffff,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_CSS_SINGLESTRING, "fore:#FDD835,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_CSS_DOUBLESTRING, "fore:#FDD835,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_CSS_IDENTIFIER, "fore:#80DEEA,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_CSS_IDENTIFIER2, "fore:#80DEEA,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_CSS_UNKNOWN_IDENTIFIER, "fore:#80DEEA,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_CSS_PSEUDOCLASS, "fore:white,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_CSS_UNKNOWN_PSEUDOCLASS, "fore:white,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_CSS_ATTRIBUTE, "fore:white,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_CSS_DIRECTIVE, "fore:white,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_CSS_IMPORTANT, "fore:white,back:#212121,face:"+self.font+",size:"+self.fontsize)
		elif self.fileext=='.xml':
			self.control.SetLexer(stc.STC_LEX_XML)
			self.control.StyleSetSpec(stc.STC_H_DEFAULT, "fore:#ffffff,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_NUMBER, "fore:#7E57C2,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_COMMENT, "fore:#616161,back:#212121,"+self.cstyle+",face:"+self.cfont+",size:"+self.cfontsize)
			self.control.StyleSetSpec(stc.STC_H_SINGLESTRING, "fore:#FDD835,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_DOUBLESTRING, "fore:#FDD835,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_XMLSTART, "fore:#D81B60,back:#212121,italic,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_XMLEND, "fore:#D81B60,back:#212121,italic,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_TAG, "fore:#D81B60,back:#212121,italic,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_TAGEND, "fore:#D81B60,back:#212121,italic,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_TAGUNKNOWN, "fore:RED,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_ATTRIBUTE, "fore:#9CCC65,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_ATTRIBUTEUNKNOWN, "fore:RED,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_OTHER, "fore:#ffffff,back:#212121,face:"+self.font+",size:"+self.fontsize)
		elif self.fileext=='.html':
			self.control.SetLexer(stc.STC_LEX_HTML)
			self.control.StyleSetSpec(stc.STC_H_DEFAULT, "fore:#ffffff,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_TAG, "fore:#D81B60,back:#212121,italic,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_TAGEND, "fore:#D81B60,back:#212121,italic,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_TAGUNKNOWN, "fore:RED,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_NUMBER, "fore:#7E57C2,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_COMMENT, "fore:#616161,back:#212121,"+self.cstyle+",face:"+self.cfont+",size:"+self.cfontsize)
			self.control.StyleSetSpec(stc.STC_H_SINGLESTRING, "fore:#FDD835,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_DOUBLESTRING, "fore:#FDD835,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_ATTRIBUTE, "fore:#9CCC65,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_ATTRIBUTEUNKNOWN, "fore:RED,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_OTHER, "fore:#FFFFFF,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_SCRIPT, "fore:RED,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_QUESTION, "fore:RED,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_VALUE, "fore:RED,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_CDATA, "fore:RED,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_ASPAT, "fore:RED,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_SGML_DEFAULT, "fore:#D81B60,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_H_SGML_ERROR, "fore:#D81B60,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_HJ_DEFAULT, "fore:RED,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_HJ_NUMBER, "fore:#7E57C2,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_HJ_SINGLESTRING, "fore:#FDD835,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_HJ_DOUBLESTRING, "fore:#FDD835,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_HJ_WORD, "fore:#9CCC65,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_HJ_SYMBOLS, "fore:#D81B60,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_HJ_COMMENT, "fore:#616161,back:#212121,"+self.cstyle+",face:"+self.cfont+",size:"+self.cfontsize)
			self.control.StyleSetSpec(stc.STC_HJ_COMMENTLINE, "fore:#616161,back:#212121,"+self.cstyle+",face:"+self.cfont+",size:"+self.cfontsize)
		elif self.fileext=='.py':
			self.control.SetLexer(stc.STC_LEX_PYTHON)
			self.control.StyleSetSpec(stc.STC_P_DEFAULT, "fore:#FFFFFF,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:#616161,back:#212121,"+self.cstyle+",face:"+self.cfont+",size:"+self.cfontsize)
			self.control.StyleSetSpec(stc.STC_P_NUMBER, "fore:#7E57C2,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_P_STRING, "fore:#FDD835,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_P_CHARACTER, "fore:#FDD835,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_P_WORD, "fore:RED,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_P_TRIPLE, "fore:#FDD835,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#FDD835,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:#D81B60,back:#212121,bold,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_P_DEFNAME, "fore:#D81B60,back:#212121,bold,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_P_OPERATOR, "fore:white,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#9CCC65,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:#616161,back:#212121,"+self.cstyle+",face:"+self.cfont+",size:"+self.cfontsize)
			self.control.StyleSetSpec(stc.STC_P_STRINGEOL, "fore:red,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_P_WORD2, "fore:red,back:#212121,face:"+self.font+",size:"+self.fontsize)
			self.control.StyleSetSpec(stc.STC_P_DECORATOR, "fore:red,back:#212121,face:"+self.font+",size:"+self.fontsize)
		else:
			pass

	def refresh(self, e):
		lines = self.control.GetLineCount()
		width = self.control.TextWidth(stc.STC_STYLE_LINENUMBER, str(lines)+"  ")
		self.control.SetMarginWidth(0, width)
		self.filetype()
		if self.control.GetModify()==True:
			if self.fileext=='.cfg':
				if self.name=='keybinds':
					self.SetTitle("Dev-Pad -- **[KEYBINDS]**" )
				elif self.name=='style':
					self.SetTitle("Dev-Pad -- **[SETTINGS]**")
				else:
					self.SetTitle("Dev-Pad -- ** %s" % self.filepath)
			else:
				self.SetTitle("Dev-Pad -- ** %s" % self.filepath)

	def statlineinfo(self,e):
		line=self.control.GetCurrentLine()
		col=self.control.GetColumn(self.control.GetCurrentPos())
		self.statusbar.SetStatusText('     Line : %s  Col : %s' % (line+1, col),0)

	def Menu(self):
		self.rtm=configparser.RawConfigParser()
		self.rtm.read('runtime')
		li=dict(self.rtm.items('recent'))
		for l in li:
			li[l]=li[l].split('#',1)[0].strip()
		globals().update(li)

		kb=configparser.RawConfigParser()
		kb.read('keybinds.cfg')
		par=dict(kb.items("keybinds"))
		for p in self.par:
		    self.par[p]=self.par[p].split("#",1)[0].strip()

		globals().update(self.par)

		menu = wx.MenuBar()
		self.SetMenuBar(menu)
		# File Menu
		file = wx.Menu(); menu.Append(file, '&File');
		new=file.Append(100,'&New'+'\t'+kb.get('keybinds','new'), 'Creates New File'); self.Bind(wx.EVT_MENU, self.new, new)
		new.SetBitmap(wx.Bitmap("icons/new.ico"))
		opens=file.Append(101,'&Open'+'\t'+kb.get('keybinds','open'), 'Browse File'); self.Bind(wx.EVT_MENU, self.opens, opens)
		opens.SetBitmap(wx.Bitmap("icons/open.ico"))
		recent=wx.Menu(); file.AppendSubMenu(recent,'Recent files')
		r1=self.rtm.get('recent','r1');r2=self.rtm.get('recent','r2');r3=self.rtm.get('recent','r3')
		r4=self.rtm.get('recent','r4');r5=self.rtm.get('recent','r5');r6=self.rtm.get('recent','r6')
		if r1!='':
			rec1=recent.Append(301,'01). '+r1); self.Bind(wx.EVT_MENU,self.openrecent1,rec1)
		if r2!='':
			rec2=recent.Append(302,'02). '+r2); self.Bind(wx.EVT_MENU,self.openrecent2,rec2)
		if r3!='':
			rec3=recent.Append(303,'03). '+r3); self.Bind(wx.EVT_MENU,self.openrecent3,rec3)
		if r4!='':
			rec4=recent.Append(304,'04). '+r4); self.Bind(wx.EVT_MENU,self.openrecent4,rec4)
		if r5!='':
			rec5=recent.Append(305,'05). '+r5); self.Bind(wx.EVT_MENU,self.openrecent5,rec5)
		if r6!='':
			rec6=recent.Append(306,'06). '+r6); self.Bind(wx.EVT_MENU,self.openrecent6,rec6)

		# recent.SetBitmap(wx.Bitmap("icons/love2.ico"))
		file.AppendSeparator()
		save=file.Append(103,'&Save'+'\t'+kb.get('keybinds','save'), 'Save the Current file'); self.Bind(wx.EVT_MENU, self.save, save)
		save.SetBitmap(wx.Bitmap("icons/save.ico"))
		saveas=file.Append(104,'Save &as'+'\t'+kb.get('keybinds','saveas'), 'Save as other doc'); self.Bind(wx.EVT_MENU,self.saveas,saveas)
		saveas.SetBitmap(wx.Bitmap("icons/saveas.ico"))
		file.AppendSeparator()
		reloadfile=file.Append(105,'Reload file')
		reloadfile.SetBitmap(wx.Bitmap("icons/reload.ico"))
		delfile=file.Append(106,'Delete file')
		delfile.SetBitmap(wx.Bitmap("icons/delete.ico"))
		file.AppendSeparator()
		exit=file.Append(999,'&Exit'+'\t'+kb.get('keybinds','exit'), 'Exit from editor'); self.Bind(wx.EVT_MENU, self.close, exit)
		exit.SetBitmap(wx.Bitmap("icons/exit2.ico"))
		# View Menu
		view = wx.Menu(); menu.Append(view, '&View')
		self.togtbar=view.AppendCheckItem(107,'Toolbar'); self.Bind(wx.EVT_MENU, self.toggletbar, self.togtbar)
		# self.togtbar.SetBitmap(wx.Bitmap("icons/font.ico"))
		self.wrapmod=view.AppendCheckItem(108,'&Wordwrap'+'\t'+kb.get('keybinds','wrap')); self.Bind(wx.EVT_MENU, self.togglewrap, self.wrapmod)
		# self.wrapmode.SetBitmap(wx.Bitmap("icons/wrap.ico"))
		self.fullscr=view.AppendCheckItem(109,'FullScreen'+'\t'+'F11'); self.Bind(wx.EVT_MENU, self.fullscreen, self.fullscr)

		if self.cfg.getboolean('settings','wrap')==True:
			self.wrapmod.Check()

		search=view.Append(110,'&Find'+'\t'+kb.get('keybinds','find')); self.Bind(wx.EVT_MENU, self.find, search)
		search.SetBitmap(wx.Bitmap("icons/find.ico"))
		# Edit Menu
		edit=wx.Menu(); menu.Append(edit,'&Edit')
		line=wx.Menu(); edit.AppendSubMenu(line,'&Line')
		goto=line.Append(111,'&Goto Line'+'\t'+kb.get('keybinds','goto')); self.Bind(wx.EVT_MENU, self.gotoline, goto)
		line.AppendSeparator()
		comm=line.Append(112, 'Comment'+'\t'+kb.get('keybinds','lcomment')); self.Bind(wx.EVT_MENU, self.comment, comm)
		dupli=line.Append(113,'&Duplicate Line'+'\t'+kb.get('keybinds','linecopy')); self.Bind(wx.EVT_MENU, self.duplicateline, dupli)
		delline=line.Append(114, 'Delete Line'+'\t'+kb.get('keybinds','delline')); self.Bind(wx.EVT_MENU, self.delline, delline)
		line.AppendSeparator()
		lineup=line.Append(115,'Move Line Up'+'\t'+kb.get('keybinds','lineup')); self.Bind(wx.EVT_MENU, self.lineup, lineup)
		linedown=line.Append(116,'Move Line Down'+'\t'+kb.get('keybinds','linedown')); self.Bind(wx.EVT_MENU, self.linedown, linedown)
		unindent=line.Append(117, 'Unindent Line'); self.Bind(wx.EVT_MENU,self.unindent,unindent)
		indent=line.Append(118, 'Indent Line'); self.Bind(wx.EVT_MENU,self.indent,indent)
		convcase=wx.Menu(); edit.AppendSubMenu(convcase,'&Convert Case')
		upcase=convcase.Append(119, '&UpperCase'+'\t'+kb.get('keybinds','lowcase')); self.Bind(wx.EVT_MENU, self.uppercase, upcase)
		locase=convcase.Append(120, '&LowerCase'+'\t'+kb.get('keybinds','upcase')); self.Bind(wx.EVT_MENU, self.lowercase, locase)
		# Settings Menu
		prefs=wx.Menu(); menu.Append(prefs, '&Preferences')
		stylesetts=prefs.Append(121,'Settings'); self.Bind(wx.EVT_MENU, self.stylesetts, stylesetts)
		stylesetts.SetBitmap(wx.Bitmap("icons/settings.ico"))
		keysetts=prefs.Append(122, 'Key Bindings'); self.Bind(wx.EVT_MENU , self.keybinds, keysetts)
		keysetts.SetBitmap(wx.Bitmap("icons/keys.ico"))

	def init(self):
		# Wrap mode
		if self.wrapmod.IsChecked()==True:
			self.control.SetWrapMode(1)
		else:
			self.control.SetWrapMode(0)

		if self.cfg.getboolean('settings','toolbar')==True:
			self.toolbar()
			self.togtbar.Check()

		rfs=configparser.RawConfigParser()
		rfs.read('runtime')
		run=dict(rfs.items("recent"))
		for l in run:
		    run[l]=run[l].split("#",1)[0].strip()

		globals().update(run)
		r1=rfs.get('recent','r1')
		if r1 != '':
			self.filepath=r1
			file = open(r1, 'r', encoding='utf-8')
			self.control.SetValue(file.read())
			self.control.SetModified(False)
			self.control.SetFocus()
			self.title()
			self.syntax()
			self.statbar()
		else:
			self.filepath=''
			self.fileext=''
			self.SetTitle('Dev-Pad')

	# Menu Tools
	def duplicateline(self,e):
		self.control.SelectionDuplicate()
	def delline(self,e):
		self.control.LineDelete()
	def lineup(self,e):
		self.control.MoveSelectedLinesUp()
	def linedown(self,e):
		self.control.MoveSelectedLinesDown()
	def uppercase(self,e):
		self.control.UpperCase()
	def lowercase(self,e):
		self.control.LowerCase()
	def unindent(self,e):
		self.control.BackTab()
	def indent(self,e):
		self.control.Tab()

	def find(self,e):
		self.control.SearchInTarget('Wrap')

	def togglewrap(self,e):
		if self.wrapmod.IsChecked()==True:
			self.control.SetWrapMode(1)
		else:
			self.control.SetWrapMode(0)

	def fullscreen(self,e):
		if self.fullscr.IsChecked()==True:
			self.ShowFullScreen(True)
		else:
			self.ShowFullScreen(False)

	def gotoline(self,e):
		dlg = wx.NumberEntryDialog(self, 'Enter line no:','Go','Goto Line',1,1,9999)
		ans=dlg.ShowModal()
		n=dlg.GetValue()
		if ans==wx.ID_OK:
			self.control.GotoLine(n-1)
		else:
			pass

	def comment(self,e):
		c=self.control.GetCurrentPos()
		l=self.control.GetCurrentLine()
		e=self.control.GetLineLength(l)
		self.control.GotoLine(l)
		if self.fileext=='.py':
			self.control.AddText('#')
			self.control.GotoPos(c+1)
		elif self.fileext=='.html':
			self.control.AddText('<!-- ')
			self.control.GotoPos(self.control.GetCurrentPos()+e)
			self.control.AddText(' -->')
			self.control.GotoPos(c+5)
		else:
			pass

	def stylesetts(self,e):
		settfile=open('style.cfg', 'r', encoding='utf-8')
		if self.control.GetModify()==True:
			dlg = wx.MessageDialog(self, 'Do you want to Save the file??','Alert',wx.YES_NO | wx.ICON_QUESTION)
			ans = dlg.ShowModal()
			if ans==wx.ID_YES:
				self.save(e)
				self.control.SetValue(settfile.read())
				self.filepath='style.cfg'
				self.control.SetModified(False)
				self.title()
				self.statbar()
				# self.syntax()
			else:
				self.control.SetValue(settfile.read())
				self.filepath='style.cfg'
				self.control.SetModified(False)
				self.title()
				self.statbar()
				# self.syntax()
		else:
			self.control.SetValue(settfile.read())
			self.filepath='style.cfg'
			self.control.SetModified(False)
			self.title()
			self.statbar()
			# self.syntax()
	def keybinds(self,e):
		keys=open('keybinds.cfg', 'r', encoding='utf-8')
		if self.control.GetModify()==True:
			dlg = wx.MessageDialog(self, 'Do you want to Save the file??','Alert',wx.YES_NO | wx.ICON_QUESTION)
			ans = dlg.ShowModal()
			if ans==wx.ID_YES:
				self.save(e)
				self.control.SetValue(keys.read())
				self.filepath='keybinds.cfg'
				self.control.SetModified(False)
				self.title()
				self.statbar()
			else:
				self.control.SetValue(keys.read())
				self.filepath='keybinds.cfg'
				self.control.SetModified(False)
				self.title()
				self.statbar()
		else:
			self.control.SetValue(keys.read())
			self.filepath='keybinds.cfg'
			self.control.SetModified(False)
			self.title()
			self.statbar()

	def toggletbar(self,e):
		if self.togtbar.IsChecked()==True:
			self.toolbar()
		else:
			self.ToolBar.Destroy()

	def toolbar(self):
		tbar=self.CreateToolBar()
		# tbar.SetBackgroundColour('#BDBDBD')
		tbar.SetBackgroundColour('#eee')
		new=tbar.AddTool(200, 'New', wx.Bitmap('icons/new.ico'))
		opens=tbar.AddTool(201, 'Open', wx.Bitmap('icons/open.ico'))
		save=tbar.AddTool(202, 'Save', wx.Bitmap('icons/save.ico'))
		# tbar.AppendSeparator()
		exit=tbar.AddTool(203, 'Exit', wx.Bitmap('icons/exit2.ico'))
		tbar.Realize()
		self.Bind(wx.EVT_TOOL, self.new, new)
		self.Bind(wx.EVT_TOOL, self.opens, opens)
		self.Bind(wx.EVT_TOOL, self.save, save)
		self.Bind(wx.EVT_TOOL, self.close, exit)

	def statbar(self):
		# self.filetype()
		if self.filepath=='untitled':
			self.statusbar.SetStatusText('          Untitled',2)
		elif self.fileext=='.cfg':
			if self.name=='keybinds':
				self.statusbar.SetStatusText('          KEYBINDS',2)
			elif self.name=='style':
				self.statusbar.SetStatusText('          SETTINGS',2)
			else:
				self.statusbar.SetStatusText('          Config(cfg) File',2)
		elif self.fileext=='.txt':
			self.statusbar.SetStatusText('          Text File',2)
		elif self.fileext=='.py':
			self.statusbar.SetStatusText('          Python Script',2)
		elif self.fileext=='.html':
			self.statusbar.SetStatusText('          HTML Page',2)
		elif self.fileext=='.css':
			self.statusbar.SetStatusText('          CSS Stylesheet',2)
		elif self.fileext=='.c':
			self.statusbar.SetStatusText('          C Program',2)
		elif self.fileext=='.cpp':
			self.statusbar.SetStatusText('          C++ Program',2)
		elif self.fileext=='.java':
			self.statusbar.SetStatusText('          JAVA Code',2)
		elif self.fileext=='.rb':
			self.statusbar.SetStatusText('          RUBY Script',2)
		elif self.fileext=='.php':
			self.statusbar.SetStatusText('          PHP Script',2)
		elif self.fileext=='.js':
			self.statusbar.SetStatusText('          JavaScript',2)
		elif self.fileext=='.xml':
			self.statusbar.SetStatusText('          XML File',2)
		else:
			self.statusbar.SetStatusText("          "+self.fileext+' File',2)

	def openrecent(self):
		file=open(self.filepath,'r',encoding='utf-8')
		self.control.SetValue(file.read())
		self.title()
		self.control.SetModified(False)
		self.runtime()
		self.statbar()
		self.syntax()
	def openrecent1(self,e):
		self.filepath=self.rtm.get('recent','r1')
		self.openrecent()
	def openrecent2(self,e):
		self.filepath=self.rtm.get('recent','r2')
		self.openrecent()
	def openrecent3(self,e):
		self.filepath=self.rtm.get('recent','r3')
		self.openrecent()
	def openrecent4(self,e):
		self.filepath=self.rtm.get('recent','r4')
		self.openrecent()
	def openrecent5(self,e):
		self.filepath=self.rtm.get('recent','r5')
		self.openrecent()
	def openrecent6(self,e):
		self.filepath=self.rtm.get('recent','r6')
		self.openrecent()

	# Main Functions
	def runtime(self):
		cfg=configparser.RawConfigParser()
		cfg.read('runtime')
		run=dict(cfg.items("recent"))
		for l in run:
		    run[l]=run[l].split("#",1)[0].strip()

		globals().update(run)
		self.r1=cfg.get('recent','r1')
		self.r2=cfg.get('recent','r2')
		self.r3=cfg.get('recent','r3')
		self.r4=cfg.get('recent','r4')
		self.r5=cfg.get('recent','r5')
		self.r6=cfg.get('recent','r6')
		if self.filepath==self.r1:
			pass
		elif self.filepath==self.r2:
			t=self.r2;self.r2=self.r1;self.r1=t
			self.write()
		elif self.filepath==self.r3:
			t=self.r3;self.r3=self.r2;self.r2=self.r1;self.r1=t
			self.write()
		elif self.filepath==self.r4:
			t=self.r4;self.r4=self.r3;self.r3=self.r2;self.r2=self.r1;self.r1=t
			self.write()
		elif self.filepath==self.r5:
			t=self.r5;self.r5=self.r4;self.r4=self.r3;self.r3=self.r2;self.r2=self.r1;self.r1=t
			self.write()
		elif self.filepath==self.r6:
			t=self.r6;self.r6=self.r5;self.r5=self.r4;self.r4=self.r3;self.r3=self.r2;self.r2=self.r1;self.r1=t
			self.write()
		else:
			self.r6=self.r5;self.r5=self.r4;self.r4=self.r3;self.r3=self.r2;self.r2=self.r1;
			cfg.set('recent','r1',self.filepath)
			cfg.set('recent','r2',self.r2)
			cfg.set('recent','r3',self.r3)
			cfg.set('recent','r4',self.r4)
			cfg.set('recent','r5',self.r5)
			cfg.set('recent','r6',self.r6)
			with open('runtime', 'w') as file:
			    cfg.write(file)
			self.Menu()

	def write(self):
		cfg=configparser.RawConfigParser()
		cfg.read('runtime')
		run=dict(cfg.items("recent"))
		for l in run:
		    run[l]=run[l].split("#",1)[0].strip()
		globals().update(run)
		cfg.set('recent','r1',self.r1)
		cfg.set('recent','r2',self.r2)
		cfg.set('recent','r3',self.r3)
		cfg.set('recent','r4',self.r4)
		cfg.set('recent','r5',self.r5)
		cfg.set('recent','r6',self.r6)
		with open('runtime', 'w') as file:
		    cfg.write(file)
		self.Menu()

	def untitled(self):
		self.control.SetValue("")
		self.filepath="untitled"
		self.title()

	def new(self, e):
		if self.control.GetModify()==True:
			dlg = wx.MessageDialog(None, 'Save & open New file??','New File',wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
			ans = dlg.ShowModal()
			if ans == wx.ID_YES:
				self.save(e)
				self.untitled()
				self.statbar()
				self.control.SetModified(False)
			elif ans==wx.ID_CANCEL:
				dlg.Destroy()
			else:
				self.untitled()
				self.statbar()
				self.control.SetModified(False)
		else:
				self.untitled()
				self.statbar()
				self.control.SetModified(False)

	def browse(self):
		files = wx.FileDialog(self, "Open File", "", "","All files (*.*)|*.*", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		ans=files.ShowModal()
		if ans== wx.ID_CANCEL:
			pass
		else:
			self.filepath=files.GetPath()
			file = open(self.filepath, 'r', encoding='utf-8')
			self.control.SetValue(file.read())
			self.title()
			self.control.SetModified(False)
			self.runtime()

	def opens(self, e):
		if self.control.GetModify()==True:
			dlg = wx.MessageDialog(self, 'Do you want to Save the file??','Alert',wx.YES_NO | wx.ICON_QUESTION)
			ans = dlg.ShowModal()
			if ans==wx.ID_YES:
				self.save(e)
				self.browse()
				self.statbar()
				self.syntax()
			else:
				self.browse()
				self.statbar()
				self.syntax()
		else:
			self.browse()
			self.statbar()
			self.syntax()

	def save(self, e):
		if self.filepath=="untitled":
			self.saveas(e)
		else:
			self.control.SaveFile(self.filepath)
			self.title()

	def saveas(self, e):
		files = wx.FileDialog(self, "Save File", "", "","All files (*.*)|*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if files.ShowModal()==wx.ID_CANCEL:
			pass
		else:
			self.filepath=files.GetPath()
			self.save(e)
			self.runtime()
			self.statbar()

	def close(self,e):
		if self.control.GetModify()==True:
			dlg = wx.MessageDialog(None, 'Click Yes to save & exit / No to exit','Exit',wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
			ans = dlg.ShowModal()
			if ans==wx.ID_YES:
				self.save(e)
				self.Destroy()
			elif ans==wx.ID_CANCEL:
				dlg.Destroy()
			else:
				self.Destroy()
		else:
			self.Destroy()

	# snippets : WriteText('text') at caret
	# self.control.AddText('devalla bharath')
	# self.control.BackTab() in curr line
	# LineCut()
	# LineTranspose() switch curr with pre
	# LoadLexerLibrary(path)
	# MarkerAdd(line,id)
	# MarkerDelete(line, id)
	# MarkerDeleteAll(id)
	# start = self.PositionFromLine(line)
    # end = self.GetLineEndPosition(line)
    # text = self.GetTextRange(start, end)

app=wx.App()
win(None)
app.MainLoop()
