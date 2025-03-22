# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from YearMonthPicker import YearMonthPicker

import gettext
_ = gettext.gettext

###########################################################################
## Class Main_Ui_Frame
###########################################################################

class Main_Ui_Frame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"壁纸更换器"), pos = wx.DefaultPosition, size = wx.Size( 500,380 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.Size( 500,380 ), wx.Size( 500,380 ) )

        bSizer6 = wx.BoxSizer( wx.VERTICAL )

        self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_panel1 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"测试" )
        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText_dirpath = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"选择壁纸目录:"), wx.DefaultPosition, wx.Size( 500,34 ), 0 )
        self.m_staticText_dirpath.Wrap( -1 )

        self.m_staticText_dirpath.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer4.Add( self.m_staticText_dirpath, 0, wx.ALL, 5 )

        self.m_dirPicker = wx.DirPickerCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, _(u"选择一个文件夹:"), wx.DefaultPosition, wx.Size( 480,38 ), wx.DIRP_DEFAULT_STYLE )
        bSizer4.Add( self.m_dirPicker, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer4, 1, wx.EXPAND, 5 )

        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"壁纸更换间隔(分钟):"), wx.DefaultPosition, wx.Size( 150,30 ), 0 )
        self.m_staticText3.Wrap( -1 )

        self.m_staticText3.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer3.Add( self.m_staticText3, 0, wx.ALL, 5 )

        self.m_spinCtrl_interval = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"30", wx.DefaultPosition, wx.Size( -1,30 ), wx.SP_ARROW_KEYS, 1, 1440, 60 )
        bSizer3.Add( self.m_spinCtrl_interval, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )

        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button_start = wx.Button( self.m_panel1, wx.ID_ANY, _(u"开始"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        bSizer2.Add( self.m_button_start, 1, wx.ALL, 5 )

        self.m_button_stop = wx.Button( self.m_panel1, wx.ID_ANY, _(u"停止"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        self.m_button_stop.Enable( False )

        bSizer2.Add( self.m_button_stop, 1, wx.ALL, 5 )

        self.m_button_prev = wx.Button( self.m_panel1, wx.ID_ANY, _(u"上一张"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        self.m_button_prev.Enable( False )

        bSizer2.Add( self.m_button_prev, 1, wx.ALL, 5 )

        self.m_button_next = wx.Button( self.m_panel1, wx.ID_ANY, _(u"下一张"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        self.m_button_next.Enable( False )

        bSizer2.Add( self.m_button_next, 1, wx.ALL, 5 )


        bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )


        bSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_checkBox_autoStart = wx.CheckBox( self.m_panel1, wx.ID_ANY, _(u"开机启动"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        bSizer61.Add( self.m_checkBox_autoStart, 1, wx.ALL, 5 )

        self.m_checkBox_startHideWin = wx.CheckBox( self.m_panel1, wx.ID_ANY, _(u"开机时隐藏窗口"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        bSizer61.Add( self.m_checkBox_startHideWin, 1, wx.ALL, 5 )

        self.m_button_exit = wx.Button( self.m_panel1, wx.ID_ANY, _(u"退出程序"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        bSizer61.Add( self.m_button_exit, 2, wx.ALL, 5 )


        bSizer1.Add( bSizer61, 0, wx.EXPAND, 5 )


        self.m_panel1.SetSizer( bSizer1 )
        self.m_panel1.Layout()
        bSizer1.Fit( self.m_panel1 )
        self.m_notebook1.AddPage( self.m_panel1, _(u"壁纸切换"), False )
        self.m_panel2 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer8 = wx.BoxSizer( wx.VERTICAL )

        bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText4 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"接口网站:"), wx.DefaultPosition, wx.Size( 70,34 ), 0 )
        self.m_staticText4.Wrap( -1 )

        self.m_staticText4.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer9.Add( self.m_staticText4, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        m_comboBox_webSiteChoices = []
        self.m_comboBox_webSite = wx.ComboBox( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 32,32 ), m_comboBox_webSiteChoices, 0 )
        bSizer9.Add( self.m_comboBox_webSite, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.m_bpButton_add_Api = wx.BitmapButton( self.m_panel2, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 32,32 ), wx.BU_AUTODRAW|0 )

        self.m_bpButton_add_Api.SetBitmap( wx.Bitmap( u"plus.png", wx.BITMAP_TYPE_ANY ) )
        bSizer9.Add( self.m_bpButton_add_Api, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_bpButton_minus_Api = wx.BitmapButton( self.m_panel2, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 32,32 ), wx.BU_AUTODRAW|0 )

        self.m_bpButton_minus_Api.SetBitmap( wx.Bitmap( u"minus.png", wx.BITMAP_TYPE_ANY ) )
        bSizer9.Add( self.m_bpButton_minus_Api, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        bSizer8.Add( bSizer9, 1, wx.EXPAND, 5 )

        bSizer10 = wx.BoxSizer( wx.VERTICAL )

        bSizer131 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText5 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"开始日期:"), wx.DefaultPosition, wx.Size( 70,34 ), 0 )
        self.m_staticText5.Wrap( -1 )

        self.m_staticText5.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer131.Add( self.m_staticText5, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_datePicker_start= YearMonthPicker(self.m_panel2, min_year=2021, min_month=2)
        bSizer131.Add( self.m_datePicker_start, 0, wx.ALL, 5 )


        bSizer10.Add( bSizer131, 0, wx.EXPAND, 5 )

        bSizer15 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText6 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"结束日期:"), wx.DefaultPosition, wx.Size( 70,34 ), 0 )
        self.m_staticText6.Wrap( -1 )

        self.m_staticText6.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer15.Add( self.m_staticText6, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_datePicker_end = YearMonthPicker(self.m_panel2, min_year=2021, min_month=2)
        bSizer15.Add( self.m_datePicker_end, 0, wx.ALL, 5 )


        bSizer10.Add( bSizer15, 0, wx.EXPAND, 5 )


        bSizer8.Add( bSizer10, 0, wx.EXPAND, 5 )

        bSizer12 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText9 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u" 保存目录: "), wx.DefaultPosition, wx.Size( 78,34 ), 0 )
        self.m_staticText9.Wrap( -1 )

        self.m_staticText9.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer12.Add( self.m_staticText9, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_textCtrl_save_folder = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        self.m_textCtrl_save_folder.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer12.Add( self.m_textCtrl_save_folder, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_button_select_Save_Folder = wx.Button( self.m_panel2, wx.ID_ANY, _(u"浏览"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        self.m_button_select_Save_Folder.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer12.Add( self.m_button_select_Save_Folder, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        bSizer8.Add( bSizer12, 0, wx.EXPAND, 5 )

        bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText7 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"分辨率："), wx.DefaultPosition, wx.Size( 70,34 ), 0 )
        self.m_staticText7.Wrap( -1 )

        self.m_staticText7.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer11.Add( self.m_staticText7, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        m_choice_resolutionChoices = [ _(u"2K"), _(u"4K") ]
        self.m_choice_resolution = wx.Choice( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,30 ), m_choice_resolutionChoices, 0 )
        self.m_choice_resolution.SetSelection( 0 )
        bSizer11.Add( self.m_choice_resolution, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_staticText8 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"下载线程数："), wx.DefaultPosition, wx.Size( 100,34 ), 0 )
        self.m_staticText8.Wrap( -1 )

        self.m_staticText8.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer11.Add( self.m_staticText8, 0, wx.ALL, 5 )

        m_choice_max_ThreadsChoices = [ _(u"2"), _(u"4"), _(u"6"), _(u"8"), _(u"10"), _(u"12"), wx.EmptyString ]
        self.m_choice_max_Threads = wx.Choice( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,30 ), m_choice_max_ThreadsChoices, 0 )
        self.m_choice_max_Threads.SetSelection( 1 )
        bSizer11.Add( self.m_choice_max_Threads, 0, wx.ALL, 5 )


        bSizer8.Add( bSizer11, 0, wx.EXPAND, 5 )

        bSizer151 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_checkBox_use_Wallpapers_Folder = wx.CheckBox( self.m_panel2, wx.ID_ANY, _(u"使用壁纸目录保存"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        self.m_checkBox_use_Wallpapers_Folder.SetValue(True)
        bSizer151.Add( self.m_checkBox_use_Wallpapers_Folder, 0, wx.ALL, 5 )

        self.m_button_start_Download = wx.Button( self.m_panel2, wx.ID_ANY, _(u"开始下载"), wx.DefaultPosition, wx.Size( 200,34 ), 0 )
        self.m_button_start_Download.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer151.Add( self.m_button_start_Download, 0, wx.ALL, 5 )

        self.m_button_exit1 = wx.Button( self.m_panel2, wx.ID_ANY, _(u"退出程序"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        bSizer151.Add( self.m_button_exit1, 1, wx.ALL, 5 )


        bSizer8.Add( bSizer151, 0, wx.EXPAND, 5 )


        self.m_panel2.SetSizer( bSizer8 )
        self.m_panel2.Layout()
        bSizer8.Fit( self.m_panel2 )
        self.m_notebook1.AddPage( self.m_panel2, _(u"壁纸下载"), True )

        bSizer6.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( bSizer6 )
        self.Layout()
        self.m_statusBar = self.CreateStatusBar( 1, wx.STB_DEFAULT_STYLE|wx.STB_SIZEGRIP, wx.ID_ANY )
        self.m_statusBar.SetFont( wx.Font( 11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_statusBar.SetMinSize( wx.Size( -1,30 ) )
        self.m_statusBar.SetMaxSize( wx.Size( -1,30 ) )


        self.Centre( wx.BOTH )

        # Connect Events
        self.m_dirPicker.Bind( wx.EVT_DIRPICKER_CHANGED, self.on_m_dirPicker_changed )
        self.m_button_start.Bind( wx.EVT_BUTTON, self.on_start )
        self.m_button_stop.Bind( wx.EVT_BUTTON, self.on_stop )
        self.m_button_prev.Bind( wx.EVT_BUTTON, self.on_prev )
        self.m_button_next.Bind( wx.EVT_BUTTON, self.on_next )
        self.m_checkBox_autoStart.Bind( wx.EVT_CHECKBOX, self.on_auto_start_changed )
        self.m_checkBox_startHideWin.Bind( wx.EVT_CHECKBOX, self.on_startHideWin_changed )
        self.m_button_exit.Bind( wx.EVT_BUTTON, self.on_exit )
        self.m_bpButton_add_Api.Bind( wx.EVT_BUTTON, self.on_bpButton_add_Api )
        self.m_bpButton_minus_Api.Bind( wx.EVT_BUTTON, self.on_bpButton_minus_Api )
        self.m_button_select_Save_Folder.Bind( wx.EVT_BUTTON, self.on_select_Save_Folder )
        self.m_checkBox_use_Wallpapers_Folder.Bind( wx.EVT_CHECKBOX, self.on_checkBox_use_Wallpapers_Folder )
        self.m_button_start_Download.Bind( wx.EVT_BUTTON, self.on_start_Download )
        self.m_button_exit1.Bind( wx.EVT_BUTTON, self.on_exit )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def on_m_dirPicker_changed( self, event ):
        event.Skip()

    def on_start( self, event ):
        event.Skip()

    def on_stop( self, event ):
        event.Skip()

    def on_prev( self, event ):
        event.Skip()

    def on_next( self, event ):
        event.Skip()

    def on_auto_start_changed( self, event ):
        event.Skip()

    def on_startHideWin_changed( self, event ):
        event.Skip()

    def on_exit( self, event ):
        event.Skip()

    def on_bpButton_add_Api( self, event ):
        event.Skip()

    def on_bpButton_minus_Api( self, event ):
        event.Skip()

    def on_select_Save_Folder( self, event ):
        event.Skip()

    def on_checkBox_use_Wallpapers_Folder( self, event ):
        event.Skip()

    def on_start_Download( self, event ):
        event.Skip()



