from datetime import datetime, timedelta
import requests
from lxml import html
import re
import os
import wx
from concurrent.futures import ThreadPoolExecutor
import threading
from app_logger import logging, RESOURCE_PATH, IS_PRODUCTION


class DownloadProcessor():

    def __init__(self, main_frame):
        self.main_frame = main_frame

    def on_bpButton_add_Api(self, event):
        """
        添加API的方法。
        此方法会获取用户输入的API地址，并将其添加到下拉框中。
        如果用户输入的API地址为空，则会弹出一个警告对话框。
        Args:
            event: 触发此方法的事件对象
        """
        logging.info("添加bing site API")
        value = self.main_frame.m_comboBox_webSite.GetValue().strip()
        if value:
            self.main_frame.m_comboBox_webSite.Append(value)
            self.main_frame.m_comboBox_webSite.SetSelection(self.main_frame.m_comboBox_webSite.GetCount() - 1)

    def on_bpButton_minus_Api(self, event):
        """
        减少API的方法。
        此方法会从下拉框中删除当前选中的API地址。
        Args:
            event: 触发此方法的事件对象
        """
        logging.info("减少bing site API")
        selected_index = self.main_frame.m_comboBox_webSite.GetSelection()
        if selected_index != wx.NOT_FOUND:
            self.main_frame.m_comboBox_webSite.Delete(selected_index)
        if self.main_frame.m_comboBox_webSite.GetCount() > 0:
            self.main_frame.m_comboBox_webSite.SetSelection(0)
        else:
            # 若为空，清空显示值
            self.main_frame.m_comboBox_webSite.SetValue('')

    def on_select_Save_Folder(self, event):
        """
        选择保存图片的文件夹,并将选择的路径显示到文本控件中。

        Args:
            event: 触发此方法的事件对象
        """
        dlg = wx.DirDialog(self.main_frame,
                           "选择保存图片的文件夹",
                           style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            selected_path = dlg.GetPath()
            self.main_frame.m_textCtrl_save_folder.SetValue(selected_path)
            logging.info(f"选择的保存路径: {selected_path}")
        dlg.Destroy()

        # 如果不使用壁纸文件夹作为壁纸下载保存目录为壁纸文件夹
        if not self.main_frame.m_checkBox_use_Wallpapers_Folder.GetValue():
            self.main_frame.save_config()

    def on_checkBox_use_Wallpapers_Folder(self, event):
        """
        处理用户选择使用壁纸文件夹的选项。
        如果用户选择了使用壁纸文件夹，则会显示一个文件夹选择对话框，
        用户可以选择保存壁纸的文件夹。
        如果用户取消选择，则会将壁纸文件夹设置为空字符串。

        Args: 触发此方法的事件对象
        """

        # 如果用户取消选择，则将壁纸文件夹设置为空字符串
        if self.main_frame.m_checkBox_use_Wallpapers_Folder.IsChecked():
            self.main_frame.m_textCtrl_save_folder.SetValue(
                self.main_frame.m_dirPicker.GetPath())
        else:
            self.main_frame.m_textCtrl_save_folder.SetValue('')
        self.main_frame.save_config()

    def on_start_Download(self, event):
        """
        开始下载壁纸的方法。
        此方法会获取用户输入的日期范围、分辨率、保存目录和最大线程数，
        并使用这些参数调用 `download_wallpapers` 函数进行壁纸下载。
        下载流程为：

        1、_validate_parameters #验证用户输入的日期范围和保存目录是否合法
        2、_start_download_process# 控制实际下载流程：
            1、_generate_months_urls #生成指定日期范围内的Bing壁纸网站每月壁纸页面URL，这个页面才有壁纸的链接
            2、_get_bing_wallpaper_links #按月份页面解析每月页面的图片链接
            3、_get_wallpaper_url_with_resolution #按分辨率修改壁纸链接
            4、_download_wallpapers #多线程下载壁纸

        Args:
            event: 触发此方法的事件对象
        """
        logging.info("开始下载壁纸")
        # 获取用户输入的日期范围
        start_date = self.main_frame.m_datePicker_start.GetValue()
        start_date = f'{start_date[0]}-{start_date[1]}'
        end_date = self.main_frame.m_datePicker_end.GetValue()
        end_date = f'{end_date[0]}-{end_date[1]}'
        web_api = self.main_frame.m_comboBox_webSite.GetValue()
        resolution = self.main_frame.m_choice_resolution.GetStringSelection()
        save_directory = self.main_frame.m_textCtrl_save_folder.GetValue()
        max_threads = int(self.main_frame.m_choice_max_Threads.GetStringSelection())
        logging.debug(f"开始日期: {start_date}, 结束日期:{end_date}")

        # 参数验证
        if not self._validate_parameters(start_date, end_date, save_directory):
            return
        # 禁用下载按钮，防止重复点击
        self.main_frame.m_button_start_Download.Disable()


        # m_statusBar
        self.main_frame.m_statusBar.SetStatusText(f"下载中...")
        # 调用下载壁纸函数
        wx.CallAfter(self._start_download_process, web_api, start_date, end_date, resolution, save_directory, max_threads)
        # self._start_download_process(web_api,start_date, end_date, resolution, save_directory, max_threads)


        self.main_frame.m_statusBar.SetStatusText(f"下载完成")
        # 启用下载按钮
        self.main_frame.m_button_start_Download.Enable()
    def _validate_parameters(self, start_date, end_date, save_directory):
        """验证输入参数"""
        try:
            start_datetime = datetime.strptime(start_date, "%Y-%m")
            end_datetime = datetime.strptime(end_date, "%Y-%m")
            if start_datetime > end_datetime:
                # wx.MessageBox("结束日期必须大于或等于开始日期", "日期错误", wx.OK | wx.ICON_ERROR)
                self.main_frame.m_statusBar.SetStatusText("结束日期必须大于或等于开始日期")
                return False
        except ValueError:
            # wx.MessageBox("日期格式无效", "日期错误", wx.OK | wx.ICON_ERROR)
            self.main_frame.m_statusBar.SetStatusText("日期格式无效")
            return False

        if not save_directory:
            # wx.MessageBox("保存目录不能为空", "目录错误", wx.OK | wx.ICON_ERROR)
            self.main_frame.m_statusBar.SetStatusText("保存目录不能为空")

            return False

        return True
    def _start_download_process(self,web_api, start_date, end_date, resolution, save_directory, max_threads):
        """
        启动真实的下载过程：
        1、生成每月页面的链接
        2、按月份页面解析每月页面的图片链接
        3、按分辨率修改壁纸链接
        4、多线程下载壁纸

        """
        try:
            self._print_run_parameters(web_api,start_date, end_date, resolution, save_directory, max_threads)
            # 生成每月页面的链接
            generated_urls = self._generate_months_urls(start_date, end_date)
            for url in generated_urls:
                logging.info(f"处理链接: {url}")
                self.main_frame.m_statusBar.SetStatusText(f"处理链接: {url}")
                # 按月份页面解析每月页面的图片链接
                wallpaper_links = self._get_bing_wallpaper_links(url)
                # 按分辨率修改壁纸链接
                logging.debug(f"---------------{resolution}")
                wallpaper_links=[
                    self._get_wallpaper_url_with_resolution(link, resolution)
                    for link in wallpaper_links
                ]
                logging.info(f"在链接{url}中发现 {len(wallpaper_links)} 个壁纸链接.")
                self.main_frame.m_statusBar.SetStatusText(f"在链接{url}中发现 {len(wallpaper_links)} 个壁纸链接.")
                #多线程下载壁纸
                self._download_wallpapers(wallpaper_links, save_directory, max_threads)
            logging.info("下载完成")
            self.main_frame.m_statusBar.SetStatusText("下载完成")
        except Exception as e:
            logging.error(f"下载错误: {str(e)}")
            self.main_frame.m_statusBar.SetStatusText(f"下载错误: {str(e)}")
        finally:
            # 重新启用下载按钮
            self.main_frame.m_button_start_Download.Enable()

    def _print_run_parameters(self, web_api, start_date, end_date, resolution, save_directory,
                              max_threads):
        """
        打印运行参数
        """
        logging.info("*" * 30)
        logging.info("运行参数:")
        logging.info(f"开始日期: {start_date}")
        logging.info(f"结束日期: {end_date}")
        logging.info(f"来源网站: {web_api}")
        logging.info(f"分辨率: {resolution}")
        logging.info(f"保存目录: {save_directory}")
        logging.info(f"最大线程数: {max_threads}")
        logging.info("*" * 30 + '\n')
    def _generate_months_urls(self, start_date, end_date):
        """
        生成指定日期范围内的Bing壁纸网站每月壁纸页面 URL

        :param start_date: 开始日期，格式为 'YYYY-MM'
        :param end_date: 结束日期，格式为 'YYYY-MM'
        :return: 生成的URL列表
        """
        urls = []
        current_date = datetime.strptime(start_date, "%Y-%m")
        end = datetime.strptime(end_date, "%Y-%m")
        web_api=self.main_frame.m_comboBox_webSite.GetValue()
        # 确保 web_api 以 / 结尾
        if not web_api.endswith('/'):
            web_api = web_api + '/'

        # 循环生成URL
        while current_date <= end:

            url = f"{web_api}{current_date.strftime('%Y-%m')}/{current_date.strftime('%Y-%m')}.html"
            urls.append(url)

            # 移到下一个月
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1,
                                                    month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)

        return urls
    def _get_bing_wallpaper_links(self, url):
        # 设置伪造的User-Agent
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # 发送HTTP请求获取网页内容
        response = requests.get(url, headers=headers)

        # 解析HTML
        tree = html.fromstring(response.content)

        # 使用XPath提取链接
        links = tree.xpath(
            "//a[@class='wallpaper_link']/@href")

        return links
    def _get_wallpaper_url_with_resolution(self,url, resolution='2k'):
        """
        根据指定的分辨率修改壁纸 URL。

        :param url: 原始壁纸 URL
        :param resolution: 分辨率，支持 '2k' 或 '4k'
        :return: 修改后的壁纸 URL
        """
        if resolution == '2k' or resolution == '2K':
            width, height = 2560, 1440
        elif resolution == '4k' or resolution == '4K':
            width, height = 3840, 2160
        else:
            width, height = 3840, 2160
            logging.error(f"{resolution}不支持的分辨率，仅支持 '2k' 或 '4k'")

        # 检查 URL 中是否已经包含 w 和 h 参数
        if 'w=' in url and 'h=' in url:
            # 如果包含，替换参数值
            url = url.replace(re.search(r'w=\d+', url).group(0), f'w={width}')
            url = url.replace(re.search(r'h=\d+', url).group(0), f'h={height}')
        else:
            # 如果不包含，添加参数
            if '?' in url:
                url = f"{url}&w={width}&h={height}"
            else:
                url = f"{url}?w={width}&h={height}"

        return url
    def _download_wallpapers(self, wallpaper_links, save_dir, max_threads=5):
        """
        使用多线程下载壁纸
        """
        # 确保保存目录存在
        os.makedirs(save_dir, exist_ok=True)

        # 创建线程池
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            # 提交下载任务
            futures = [
                executor.submit(self._download_wallpaper, url, save_dir)
                for url in wallpaper_links
            ]

            # 等待所有任务完成
            for future in futures:
                future.result()
    def _download_wallpaper(self, url, save_dir):
        """
        下载壁纸并保存到指定目录
        """
        try:
            # 从URL中提取文件名
            file_name = url.split('id=')[1].split('&')[0]
            file_path = os.path.join(save_dir, file_name)

            # 发送GET请求下载图片
            # 设置伪造的User-Agent
            headers = {
                'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, stream=True, headers=headers)
            response.raise_for_status()  # 如果请求不成功则抛出异常

            # 保存图片
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            logging.info(f"保存名: {file_name}\n下载链接：{url}")
        except Exception as e:
            logging.error(f"下载错误： {url}: {str(e)}")