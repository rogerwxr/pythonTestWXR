import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os


class TestBaiduSearchLocal:
    # @pytest.fixture(autouse=True)
    # def setup_method(self):
    #     # --- 配置区域 ---
    #     # 方案 A: 如果 chromedriver 就在当前脚本同级目录下 (推荐)
    #     current_dir = os.path.dirname(os.path.abspath(__file__))
    #     driver_path = os.path.join(current_dir, "chromedriver.exe")  # Windows 用 .exe, Mac/Linux 去掉 .exe
    #
    #     if not os.path.exists(driver_path):
    #         raise FileNotFoundError(
    #             f"未在路径找到 chromedriver: {driver_path}\n"
    #             "请确保已手动下载 chromedriver 并放在脚本同级目录，或修改代码中的路径。"
    #         )
    #
    #     # --- 启动浏览器 ---
    #     options = webdriver.ChromeOptions()
    #     # options.add_argument("--headless") # 如果需要无头模式（不显示界面），取消这行注释
    #
    #     self.driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=options)
    #     self.driver.maximize_window()
    #     self.driver.implicitly_wait(10)
    #
    #     yield
    #
    #     self.driver.quit()

    def test_baidu_search_fast(self):
        """测试百度搜索功能"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        driver_path = os.path.join(current_dir, "chromedriver.exe")  # Windows 用 .exe, Mac/Linux 去掉 .exe

        if not os.path.exists(driver_path):
            raise FileNotFoundError(
                f"未在路径找到 chromedriver: {driver_path}\n"
                "请确保已手动下载 chromedriver 并放在脚本同级目录，或修改代码中的路径。"
            )

        # --- 启动浏览器 ---
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless") # 如果需要无头模式（不显示界面），取消这行注释

        self.driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        # yield

        self.driver.quit()

        self.driver.get("https://www.baidu.com")

        # 定位搜索框 (百度搜索框 ID 通常为 kw)
        search_box = self.driver.find_element(By.ID, "chat-textarea")
        search_box.send_keys("Selenium 本地驱动测试")

        # 定位搜索按钮 (百度搜索按钮 ID 通常为 su)
        search_button = self.driver.find_element(By.ID, "chat-submit-button")
        search_button.click()

        # 验证标题
        assert "Selenium" in self.driver.title
        print(f"✅ 测试成功！标题: {self.driver.title}")