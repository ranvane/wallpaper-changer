# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class Main_Ui_Frame
###########################################################################

class Main_Ui_Frame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"壁纸更换器"), pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText_dirpath = wx.StaticText( self, wx.ID_ANY, _(u"选择壁纸目录:"), wx.DefaultPosition, wx.Size( 500,30 ), 0 )
        self.m_staticText_dirpath.Wrap( -1 )

        self.m_staticText_dirpath.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer4.Add( self.m_staticText_dirpath, 0, wx.ALL, 5 )

        self.m_dirPicker = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, _(u"选择一个文件夹:"), wx.DefaultPosition, wx.Size( 480,30 ), wx.DIRP_DEFAULT_STYLE )
        bSizer4.Add( self.m_dirPicker, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer4, 1, wx.EXPAND, 5 )

        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, _(u"壁纸更换间隔(分钟):"), wx.DefaultPosition, wx.Size( 150,30 ), 0 )
        self.m_staticText3.Wrap( -1 )

        self.m_staticText3.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer3.Add( self.m_staticText3, 0, wx.ALL, 5 )

        self.m_spinCtrl_interval = wx.SpinCtrl( self, wx.ID_ANY, u"30", wx.DefaultPosition, wx.Size( -1,30 ), wx.SP_ARROW_KEYS, 1, 1440, 60 )
        bSizer3.Add( self.m_spinCtrl_interval, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )

        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button_start = wx.Button( self, wx.ID_ANY, _(u"开始"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        bSizer2.Add( self.m_button_start, 1, wx.ALL, 5 )

        self.m_button_stop = wx.Button( self, wx.ID_ANY, _(u"停止"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        self.m_button_stop.Enable( False )

        bSizer2.Add( self.m_button_stop, 1, wx.ALL, 5 )

        self.m_button_prev = wx.Button( self, wx.ID_ANY, _(u"上一张"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        self.m_button_prev.Enable( False )

        bSizer2.Add( self.m_button_prev, 1, wx.ALL, 5 )

        self.m_button_next = wx.Button( self, wx.ID_ANY, _(u"下一张"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        self.m_button_next.Enable( False )

        bSizer2.Add( self.m_button_next, 1, wx.ALL, 5 )


        bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )

        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_checkBox_autoStart = wx.CheckBox( self, wx.ID_ANY, _(u"开机启动"), wx.DefaultPosition, wx.Size( -1,34 ), 0 )
        bSizer6.Add( self.m_checkBox_autoStart, 1, wx.ALL, 5 )

        self.m_button_exit = wx.Button( self, wx.ID_ANY, _(u"退出程序"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.m_button_exit, 1, wx.ALL, 5 )


        bSizer1.Add( bSizer6, 1, wx.EXPAND, 5 )

        self.m_staticText_status = wx.StaticText( self, wx.ID_ANY, _(u"当前壁纸: "), wx.DefaultPosition, wx.Size( 500,30 ), 0 )
        self.m_staticText_status.Wrap( -1 )

        self.m_staticText_status.SetFont( wx.Font( 11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer1.Add( self.m_staticText_status, 0, wx.ALL, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.m_dirPicker.Bind( wx.EVT_DIRPICKER_CHANGED, self.on_m_dirPicker_changed )
        self.m_button_start.Bind( wx.EVT_BUTTON, self.on_start )
        self.m_button_stop.Bind( wx.EVT_BUTTON, self.on_stop )
        self.m_button_prev.Bind( wx.EVT_BUTTON, self.on_prev )
        self.m_button_next.Bind( wx.EVT_BUTTON, self.on_next )
        self.m_checkBox_autoStart.Bind( wx.EVT_CHECKBOX, self.on_auto_start_changed )
        self.m_button_exit.Bind( wx.EVT_BUTTON, self.on_exit )

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

    def on_exit( self, event ):
        event.Skip()


