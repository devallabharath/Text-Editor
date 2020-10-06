import wx
import configparser

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
	recent.AppendSeparator()
	remre=recent.Append(103,'Clear recents'); self.Bind(wx.EVT_MENU,self.rem_recents,remre)
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
