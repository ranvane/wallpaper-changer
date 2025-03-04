from datetime import datetime, timedelta
import requests
from lxml import html
import re
import os
import wx
from concurrent.futures import ThreadPoolExecutor
import threading
from my_logger import logger, RESOURCE_PATH, IS_PRODUCTION



class DownloadProcessor():

    def __init__(self, main_frame):
        self.main_frame = main_frame

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
            logger.info(f"选择的保存路径: {selected_path}")
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
        Args:
            event: 触发此方法的事件对象
        """
        logger.info("开始下载壁纸")
        # 获取用户输入的日期范围
        start_date = self.main_frame.m_datePicker_start.GetValue()
        start_date = f'{start_date[0]}-{start_date[1]}'
        end_date = self.main_frame.m_datePicker_end.GetValue()
        end_date = f'{end_date[0]}-{end_date[1]}'
        resolution = self.main_frame.m_choice_resolution.GetStringSelection()
        save_directory = self.main_frame.m_textCtrl_save_folder.GetValue()
        max_threads = int(self.main_frame.m_choice_max_Threads.GetStringSelection())
        logger.debug(f"开始日期: {start_date}, 结束日期:{end_date}")
        
        # 参数验证
        if not self._validate_parameters(start_date, end_date, save_directory):
            return
        # 禁用下载按钮，防止重复点击
        self.main_frame.m_button_start_Download.Disable()
        self._print_run_parameters(start_date, end_date, resolution, save_directory,
                             max_threads)
        
        # m_statusBar
        self.main_frame.m_statusBar.SetStatusText(f"下载中...")
        # 调用下载壁纸函数
        self._start_download_process(start_date, end_date, resolution, save_directory, max_threads)
        # 启用下载按钮

        self.main_frame.m_statusBar.SetStatusText(f"下载完成")


    def _download_wallpaper(self,url, save_dir):
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

            logger.info(f"保存名: {file_name}\n下载链接：{url}")
        except Exception as e:
            logger.error(f"下载错误： {url}: {str(e)}")


    def _download_wallpapers(self,wallpaper_links, save_dir, max_threads=5):
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


    def _get_bing_wallpaper_links(self,url, resolution='2k'):
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
            "//div[@id='img_list']/div[@class='w3-third ']/p/a/@href")

        # 根据分辨率设置参数
        if resolution == '4k':
            width, height = 3840, 2160
        else:  # 默认为2k
            width, height = 2560, 1440

        # 修改链接中的分辨率参数
        modified_links = []
        for link in links:
            # 使用正则表达式替换宽度和高度
            modified_link = re.sub(r'w=\d+&h=\d+', f'w={width}&h={height}', link)
            modified_links.append(modified_link)

        return modified_links


    def _generate_wdbyte_urls(self,start_date, end_date):
        """
        生成指定日期范围内的Bing壁纸网站wdbyte.com URL

        :param start_date: 开始日期，格式为 'YYYY-MM'
        :param end_date: 结束日期，格式为 'YYYY-MM'
        :return: 生成的URL列表
        """
        urls = []
        current_date = datetime.strptime(start_date, "%Y-%m")
        end = datetime.strptime(end_date, "%Y-%m")

        while current_date <= end:
            url = f"https://bing.wdbyte.com/{current_date.strftime('%Y-%m')}"
            urls.append(url)

            # 移到下一个月
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1,
                                                    month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)

        return urls


    def _print_run_parameters(self,start_date, end_date, resolution, save_directory,
                            max_threads):
        """
        打印运行参数
        """
        logger.info("*" * 30)
        logger.info("运行参数:")
        logger.info(f"开始日期: {start_date}")
        logger.info(f"结束日期: {end_date}")
        logger.info(f"分辨率: {resolution}")
        logger.info(f"保存目录: {save_directory}")
        logger.info(f"最大线程数: {max_threads}")
        logger.info("*" * 30 + '\n')


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
    def _start_download_process(self, start_date, end_date, resolution, save_directory, max_threads):
        """启动下载过程"""
        try:
            self._print_run_parameters(start_date, end_date, resolution, save_directory, max_threads)
            
            generated_urls = self._generate_wdbyte_urls(start_date, end_date)
            for url in generated_urls:
                logger.info(f"处理链接: {url}")
                self.main_frame.m_statusBar.SetStatusText(f"处理链接: {url}")
                
                wallpaper_links = self._get_bing_wallpaper_links(url, resolution)
                logger.info(f"在链接{url}中发现 {len(wallpaper_links)} 个壁纸链接.")
                self.main_frame.m_statusBar.SetStatusText(f"在链接{url}中发现 {len(wallpaper_links)} 个壁纸链接.")
                

                self._download_wallpapers(wallpaper_links, save_directory, max_threads)

            self.main_frame.m_statusBar.SetStatusText("下载完成")
        except Exception as e:
            logger.error(f"下载错误: {str(e)}")
            self.main_frame.m_statusBar.SetStatusText(f"下载错误: {str(e)}")
        finally:
            # 重新启用下载按钮
            self.main_frame.m_button_start_Download.Enable()