import os
import wx
import wx.stc as stc
import configparser
import style, syntax

class win(wx.Frame):

	def __init__(self, *args, **kwargs):
		super(win, self).__init__(*args, **kwargs)
		self.Show()
		self.SetIcon(wx.Icon("icons/icon.ico"))
		# self.SetSize(1000,600)
		self.Center()
		# self.Move(90,50)
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

		remre=file.Append(103,'Clear recents'); self.Bind(wx.EVT_MENU,self.rem_recents,remre)

		# recent.SetBitmap(wx.Bitmap("icons/love2.ico"))
		file.AppendSeparator()
		save=file.Append(104,'&Save'+'\t'+kb.get('keybinds','save'), 'Save the Current file'); self.Bind(wx.EVT_MENU, self.save, save)
		save.SetBitmap(wx.Bitmap("icons/save.ico"))
		saveas=file.Append(105,'Save &as'+'\t'+kb.get('keybinds','saveas'), 'Save as other doc'); self.Bind(wx.EVT_MENU,self.saveas,saveas)
		saveas.SetBitmap(wx.Bitmap("icons/saveas.ico"))
		file.AppendSeparator()
		reloadfile=file.Append(106,'Reload file')
		reloadfile.SetBitmap(wx.Bitmap("icons/reload.ico"))
		delfile=file.Append(107,'Delete file')
		delfile.SetBitmap(wx.Bitmap("icons/delete.ico"))
		file.AppendSeparator()
		exit=file.Append(999,'&Exit'+'\t'+kb.get('keybinds','exit'), 'Exit from editor'); self.Bind(wx.EVT_MENU, self.close, exit)
		exit.SetBitmap(wx.Bitmap("icons/exit2.ico"))
		# View Menu
		view = wx.Menu(); menu.Append(view, '&View')
		self.togtbar=view.AppendCheckItem(108,'Toolbar'); self.Bind(wx.EVT_MENU, self.toggletbar, self.togtbar)
		# self.togtbar.SetBitmap(wx.Bitmap("icons/font.ico"))
		self.wrapmod=view.AppendCheckItem(109,'&Wordwrap'+'\t'+kb.get('keybinds','wrap')); self.Bind(wx.EVT_MENU, self.togglewrap, self.wrapmod)
		# self.wrapmode.SetBitmap(wx.Bitmap("icons/wrap.ico"))
		self.fullscr=view.AppendCheckItem(110,'FullScreen'+'\t'+'F11'); self.Bind(wx.EVT_MENU, self.fullscreen, self.fullscr)

		if self.cfg.getboolean('settings','wrap')==True:
			self.wrapmod.Check()

		search=view.Append(111,'&Find'+'\t'+kb.get('keybinds','find')); self.Bind(wx.EVT_MENU, self.find, search)
		search.SetBitmap(wx.Bitmap("icons/find.ico"))
		# Edit Menu
		edit=wx.Menu(); menu.Append(edit,'&Edit')
		line=wx.Menu(); edit.AppendSubMenu(line,'&Line')
		goto=line.Append(112,'&Goto Line'+'\t'+kb.get('keybinds','goto')); self.Bind(wx.EVT_MENU, self.gotoline, goto)
		line.AppendSeparator()
		comm=line.Append(113, 'Comment'+'\t'+kb.get('keybinds','lcomment')); self.Bind(wx.EVT_MENU, self.comment, comm)
		dupli=line.Append(114,'&Duplicate Line'+'\t'+kb.get('keybinds','linecopy')); self.Bind(wx.EVT_MENU, self.duplicateline, dupli)
		delline=line.Append(115, 'Delete Line'+'\t'+kb.get('keybinds','delline')); self.Bind(wx.EVT_MENU, self.delline, delline)
		line.AppendSeparator()
		lineup=line.Append(116,'Move Line Up'+'\t'+kb.get('keybinds','lineup')); self.Bind(wx.EVT_MENU, self.lineup, lineup)
		linedown=line.Append(117,'Move Line Down'+'\t'+kb.get('keybinds','linedown')); self.Bind(wx.EVT_MENU, self.linedown, linedown)
		unindent=line.Append(118, 'Unindent Line'); self.Bind(wx.EVT_MENU,self.unindent,unindent)
		indent=line.Append(119, 'Indent Line'); self.Bind(wx.EVT_MENU,self.indent,indent)
		convcase=wx.Menu(); edit.AppendSubMenu(convcase,'&Convert Case')
		upcase=convcase.Append(120, '&UpperCase'+'\t'+kb.get('keybinds','lowcase')); self.Bind(wx.EVT_MENU, self.uppercase, upcase)
		locase=convcase.Append(121, '&LowerCase'+'\t'+kb.get('keybinds','upcase')); self.Bind(wx.EVT_MENU, self.lowercase, locase)
		# Settings Menu
		prefs=wx.Menu(); menu.Append(prefs, '&Preferences')
		stylesetts=prefs.Append(122,'Settings'); self.Bind(wx.EVT_MENU, self.stylesetts, stylesetts)
		stylesetts.SetBitmap(wx.Bitmap("icons/settings.ico"))
		keysetts=prefs.Append(123, 'Key Bindings'); self.Bind(wx.EVT_MENU , self.keybinds, keysetts)
		keysetts.SetBitmap(wx.Bitmap("icons/keys.ico"))

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
				file = open(r1, 'r', encoding='utf-8')
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
			self.Menu()

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
