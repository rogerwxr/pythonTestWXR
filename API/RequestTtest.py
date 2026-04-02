import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_get_posts():
    """测试获取所有文章"""
    response = requests.get(f"{BASE_URL}/posts")
    
    # 断言1: 检查状态码是否为 200
    assert response.status_code == 200, "请求失败，状态码不是 200"
    
    # 断言2: 检查返回的数据是否为列表
    assert isinstance(response.json(), list), "返回的数据不是列表"
    
    # 断言3: 检查列表中的第一项是否包含 'title' 字段
    assert "title" in response.json()[0], "返回的数据项缺少 'title' 字段"

def test_create_post():
    """测试创建一篇新文章"""
    payload = {
        "title": "我的测试文章",
        "body": "这是文章内容",
        "userId": 1
    }
    response = requests.post(f"{BASE_URL}/posts", json=payload)
    
    # 断言1: 检查状态码是否为 201 (已创建)
    assert response.status_code == 201, "创建失败，状态码不是 201"
    
    # 断言2: 检查返回的标题是否与发送的一致
    assert response.json()["title"] == payload["title"], "返回的标题与发送的不一致"

def test_get_nonexistent_post():
    """测试获取不存在的文章"""
    response = requests.get(f"{BASE_URL}/posts/9999")
    
    # 断言: 检查状态码是否为 404 (未找到)
    assert response.status_code == 404, "请求不存在的资源，状态码不是 404"