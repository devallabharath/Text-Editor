import os
import wx
import wx.stc as stc
import configparser
import style, syntax, menu

class win(wx.Frame):

	def __init__(self, *args, **kwargs):
		super(win, self).__init__(*args, **kwargs)
		self.Show()
		self.SetIcon(wx.Icon("icons/icon.ico"))
		self.Center()
		# self.SetSize(1000,600)
		self.Maximize(True)

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
		menu.Menu(self)
		style.style(self)
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

	def stylesetts(self,e):
		settfile=open('style.cfg', 'r')
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
			else:
				self.control.SetValue(settfile.read())
				self.filepath='style.cfg'
				self.control.SetModified(False)
				self.title()
				self.statbar()
		else:
			self.control.SetValue(settfile.read())
			self.filepath='style.cfg'
			self.control.SetModified(False)
			self.title()
			self.statbar()

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

	def init(self):
		# Wrap mode
		if self.wrapmod.IsChecked()==True:
			self.control.SetWrapMode(1)
		else:
			self.control.SetWrapMode(0)

		if wx.Platform == '__WXMSW__':
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
			try :
				self.filepath=r1
				file = open(r1, 'r')
				self.control.SetValue(file.read())
				self.control.SetModified(False)
				self.control.SetFocus()
				self.title()
				syntax.syntax(self)
				self.statbar()
			except:
				self.filepath='untitled'
				self.fileext=''
				self.title()
		else:
			self.filepath='untitled'
			self.fileext=''
			self.SetTitle('Dev-Pad')

	def keybinds(self,e):
		keys=open('keybinds.cfg', 'r')
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
		file=open(self.filepath,'r')
		self.control.SetValue(file.read())
		self.title()
		self.control.SetModified(False)
		self.runtime()
		self.statbar()
		syntax.syntax(self)
	def openrecent1(self,e):
		try:
			self.filepath=self.rtm.get('recent','r1')
			self.openrecent()
		except:
			pass
	def openrecent2(self,e):
		try:
			self.filepath=self.rtm.get('recent','r2')
			self.openrecent()
		except:
			pass
	def openrecent3(self,e):
		try:
			self.filepath=self.rtm.get('recent','r3')
			self.openrecent()
		except:
			pass
	def openrecent4(self,e):
		try:
			self.filepath=self.rtm.get('recent','r4')
			self.openrecent()
		except:
			pass
	def openrecent5(self,e):
		try:
			self.filepath=self.rtm.get('recent','r5')
			self.openrecent()
		except:
			pass
	def openrecent6(self,e):
		try:
			self.filepath=self.rtm.get('recent','r6')
			self.openrecent()
		except:
			pass

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
			menu.Menu(self)

	def rem_recents(self,e):
		self.r1=self.filepath
		self.r2=self.r3=self.r4=self.r5=self.r6=''
		self.write()

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
		menu.Menu(self)

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
			file = open(self.filepath, 'r')
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
				syntax.syntax(self)
			else:
				self.browse()
				self.statbar()
				syntax.syntax(self)
		else:
			self.browse()
			self.statbar()
			syntax.syntax(self)

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


app=wx.App()
win(None)
app.MainLoop()
