# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.adv
import wx.richtext

import gettext
_ = gettext.gettext

###########################################################################
## Class Main_Ui_Frame
###########################################################################

class Main_Ui_Frame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"壁纸更换器"), pos = wx.DefaultPosition, size = wx.Size( 500,350 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer6 = wx.BoxSizer( wx.VERTICAL )

        self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_panel1 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"测试" )
        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText_dirpath = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"选择壁纸目录:"), wx.DefaultPosition, wx.Size( 500,30 ), 0 )
        self.m_staticText_dirpath.Wrap( -1 )

        self.m_staticText_dirpath.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer4.Add( self.m_staticText_dirpath, 0, wx.ALL, 5 )

        self.m_dirPicker = wx.DirPickerCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, _(u"选择一个文件夹:"), wx.DefaultPosition, wx.Size( 480,30 ), wx.DIRP_DEFAULT_STYLE )
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

        bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_checkBox_autoStart = wx.CheckBox( self.m_panel1, wx.ID_ANY, _(u"开机启动"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        bSizer61.Add( self.m_checkBox_autoStart, 1, wx.ALL, 5 )

        self.m_checkBox_startHideWin = wx.CheckBox( self.m_panel1, wx.ID_ANY, _(u"开机时隐藏窗口"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        bSizer61.Add( self.m_checkBox_startHideWin, 1, wx.ALL, 5 )

        self.m_button_exit = wx.Button( self.m_panel1, wx.ID_ANY, _(u"退出程序"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer61.Add( self.m_button_exit, 2, wx.ALL, 5 )


        bSizer1.Add( bSizer61, 1, wx.EXPAND, 5 )

        self.m_staticText_status = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"当前壁纸: "), wx.DefaultPosition, wx.Size( 500,30 ), 0 )
        self.m_staticText_status.Wrap( -1 )

        self.m_staticText_status.SetFont( wx.Font( 11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer1.Add( self.m_staticText_status, 0, wx.ALL, 5 )


        self.m_panel1.SetSizer( bSizer1 )
        self.m_panel1.Layout()
        bSizer1.Fit( self.m_panel1 )
        self.m_notebook1.AddPage( self.m_panel1, _(u"壁纸切换"), False )
        self.m_panel2 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer8 = wx.BoxSizer( wx.VERTICAL )

        bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText4 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"接口网站:"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        self.m_staticText4.Wrap( -1 )

        self.m_staticText4.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer9.Add( self.m_staticText4, 0, wx.ALL, 5 )

        m_comboBox1Choices = []
        self.m_comboBox1 = wx.ComboBox( self.m_panel2, wx.ID_ANY, _(u"wdbyte.com"), wx.DefaultPosition, wx.Size( -1,34 ), m_comboBox1Choices, 0 )
        bSizer9.Add( self.m_comboBox1, 0, wx.ALL, 5 )


        bSizer8.Add( bSizer9, 0, wx.EXPAND, 5 )

        bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText5 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"开始日期:"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        self.m_staticText5.Wrap( -1 )

        self.m_staticText5.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer10.Add( self.m_staticText5, 0, wx.ALL, 5 )

        self.m_datePicker_start = wx.adv.DatePickerCtrl( self.m_panel2, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.Size( -1,34 ), wx.adv.DP_DEFAULT )
        self.m_datePicker_start.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer10.Add( self.m_datePicker_start, 1, wx.ALL, 5 )

        self.m_staticText6 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"结束日期:"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        self.m_staticText6.Wrap( -1 )

        self.m_staticText6.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer10.Add( self.m_staticText6, 0, wx.ALL, 5 )

        self.m_datePicker_end = wx.adv.DatePickerCtrl( self.m_panel2, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.Size( -1,34 ), wx.adv.DP_ALLOWNONE|wx.adv.DP_DEFAULT|wx.adv.DP_DROPDOWN|wx.adv.DP_SHOWCENTURY )
        self.m_datePicker_end.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer10.Add( self.m_datePicker_end, 1, wx.ALL, 5 )


        bSizer8.Add( bSizer10, 0, wx.EXPAND, 5 )

        bSizer12 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText9 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u" 保存目录: "), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        self.m_staticText9.Wrap( -1 )

        self.m_staticText9.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer12.Add( self.m_staticText9, 0, wx.ALL, 5 )

        self.m_textCtrl_save_folder = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        self.m_textCtrl_save_folder.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer12.Add( self.m_textCtrl_save_folder, 1, wx.ALL, 5 )

        self.m_button_select_Save_Folder = wx.Button( self.m_panel2, wx.ID_ANY, _(u"浏览"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        self.m_button_select_Save_Folder.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer12.Add( self.m_button_select_Save_Folder, 0, wx.ALL, 5 )


        bSizer8.Add( bSizer12, 0, wx.EXPAND, 5 )

        bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText7 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"分辨率："), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        self.m_staticText7.Wrap( -1 )

        self.m_staticText7.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer11.Add( self.m_staticText7, 0, wx.ALL, 5 )

        m_choice_resolutionChoices = [ _(u"2K"), _(u"4K") ]
        self.m_choice_resolution = wx.Choice( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,34 ), m_choice_resolutionChoices, 0 )
        self.m_choice_resolution.SetSelection( 0 )
        bSizer11.Add( self.m_choice_resolution, 0, wx.ALL, 5 )

        self.m_staticText8 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"下载线程数："), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        self.m_staticText8.Wrap( -1 )

        self.m_staticText8.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer11.Add( self.m_staticText8, 0, wx.ALL, 5 )

        m_choice_max_ThreadsChoices = [ _(u"2"), _(u"4"), _(u"6"), _(u"8"), _(u"10"), _(u"12"), wx.EmptyString ]
        self.m_choice_max_Threads = wx.Choice( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,34 ), m_choice_max_ThreadsChoices, 0 )
        self.m_choice_max_Threads.SetSelection( 1 )
        bSizer11.Add( self.m_choice_max_Threads, 0, wx.ALL, 5 )

        self.m_button_start_Download = wx.Button( self.m_panel2, wx.ID_ANY, _(u"开始下载"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        self.m_button_start_Download.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer11.Add( self.m_button_start_Download, 1, wx.ALL, 5 )


        bSizer8.Add( bSizer11, 0, wx.EXPAND, 5 )

        bSizer13 = wx.BoxSizer( wx.VERTICAL )

        self.m_richText_log = wx.richtext.RichTextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
        bSizer13.Add( self.m_richText_log, 1, wx.EXPAND |wx.ALL, 5 )


        bSizer8.Add( bSizer13, 1, wx.EXPAND, 5 )


        self.m_panel2.SetSizer( bSizer8 )
        self.m_panel2.Layout()
        bSizer8.Fit( self.m_panel2 )
        self.m_notebook1.AddPage( self.m_panel2, _(u"壁纸下载"), True )

        bSizer6.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( bSizer6 )
        self.Layout()

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
        self.m_button_select_Save_Folder.Bind( wx.EVT_BUTTON, self.on_select_Save_Folder )

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

    def on_select_Save_Folder( self, event ):
        event.Skip()


