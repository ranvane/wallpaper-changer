import wx
import wx.adv


class YearMonthPicker(wx.Panel):
    def __init__(self, parent, min_year=2021, min_month=2, id=wx.ID_ANY, *args, **kwargs):
        """
            初始化YearMonthPicker控件。

            :param parent: 父窗口
            :param min_year: 最小可选年份，默认为2021
            :param min_month: 最小可选月份，默认为2
            :param id: 控件ID
            :param args: 额外的位置参数
            :param kwargs: 额外的关键字参数
        """
        super(YearMonthPicker, self).__init__(parent, id, *args, **kwargs)

        # 获取当前年份和月份
        now = wx.DateTime.Now()
        self.current_year = now.GetYear()
        self.current_month = now.GetMonth() + 1  # wx.DateTime 的 GetMonth() 返回 0-11，所以需要 +1

        # 记录最小可选年月
        self.min_year = min_year
        self.min_month = min_month

        # 创建年份选择控件（仅允许选择 min_year ~ current_year）
        self.year_combo = wx.ComboBox(self, size=(100, 25), style=wx.CB_READONLY)
        self.year_combo.AppendItems([str(year) for year in range(self.min_year, self.current_year + 1)])
        self.year_combo.SetValue(str(self.current_year))  # 默认当前年份

        # 创建月份选择控件（稍后根据年份动态更新可选范围）
        self.month_combo = wx.ComboBox(self, size=(80, 25), style=wx.CB_READONLY)
        self.update_month_choices(self.current_year, self.current_month)
        self.month_combo.SetValue(f"{self.current_month:02d}")  # 默认当前月份

        # 创建一个文本控件来显示选中的年月
        # self.text_ctrl = wx.TextCtrl(self, style=wx.TE_READONLY, size=(100, 25))

        # 布局管理
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.year_combo, 0, wx.ALL, 5)
        sizer.Add(self.month_combo, 0, wx.ALL, 5)
        # sizer.Add(self.text_ctrl, 0, wx.ALL, 5)

        self.SetSizer(sizer)
        self.SetSizerAndFit(sizer)
        self.Layout()

        # 绑定事件处理
        self.year_combo.Bind(wx.EVT_COMBOBOX, self.on_year_changed)
        self.month_combo.Bind(wx.EVT_COMBOBOX, self.on_date_changed)

        # 初始化显示
        self.update_display()

    def on_year_changed(self, event):
        """当年份改变时，更新可选的月份范围"""
        selected_year = int(self.year_combo.GetValue())

        # 获取当前年月
        now = wx.DateTime.Now()
        current_year = now.GetYear()
        current_month = now.GetMonth() + 1

        # 更新月份选择框的选项
        self.update_month_choices(selected_year, current_month)

        # 触发一次日期更新
        self.update_display()

    def on_date_changed(self, event):
        """当月份改变时，更新文本框显示"""
        # self.update_display()
        pass

    def update_month_choices(self, selected_year, current_month):
        """根据所选年份更新月份选择框"""
        self.month_combo.Clear()

        if selected_year == self.min_year:
            start_month = self.min_month  # 最小年份时，从最小月份开始
        else:
            start_month = 1  # 其他年份，从1月开始

        if selected_year == self.current_year:
            end_month = current_month  # 最大年份时，最大可选月份为当前月份
        else:
            end_month = 12  # 其他年份，可选到12月

        # 添加可选的月份
        self.month_combo.AppendItems([f"{i:02d}" for i in range(start_month, end_month + 1)])

        # 确保月份选择框的值合法
        current_selected_month = int(self.month_combo.GetValue()) if self.month_combo.GetValue() else start_month
        if current_selected_month < start_month or current_selected_month > end_month:
            self.month_combo.SetValue(f"{start_month:02d}")  # 重置为可选范围的第一个月份
        else:
            self.month_combo.SetValue(f"{current_selected_month:02d}")  # 保持原选择值

    def update_display(self):
        """更新文本框显示选中的年月"""
        selected_year = self.year_combo.GetValue()
        selected_month = self.month_combo.GetValue()
        formatted_date = f"{selected_year}-{selected_month}"
        # self.text_ctrl.SetValue(formatted_date)

    def GetValue(self):
        """获取当前选中的年月"""
        selected_year = self.year_combo.GetValue()
        selected_month = self.month_combo.GetValue()
        return (selected_year, selected_month)

    def SetValue(self, year, month):
        """设置当前选中的年月"""
        self.year_combo.SetValue(year)
        self.month_combo.SetValue(month)


# 示例用法
class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # 创建自定义的年-月选择控件，最小可选时间为2021年2月
        self.year_month_picker = YearMonthPicker(panel, min_year=2021, min_month=2)

        # 将控件添加到布局中
        sizer.Add(self.year_month_picker, 0, wx.ALL, 10)

        panel.SetSizer(sizer)

        self.SetSize((350, 150))
        self.SetTitle('自定义 年-月 选择器')
        self.Centre()


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None)
        frame.Show()
        return True


if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
