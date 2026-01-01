#!/usr/bin/env python3
"""
Obico ML API 检测测试脚本
用于测试 Obico ML 服务端的可用性
"""

import requests
import json
import sys

# ==================== 配置区域 (手动修改这里) ====================
# Obico ML API 服务器地址
OBICO_HOST = "http://100.64.0.2:33333"

# 认证令牌
AUTH_TOKEN = "example_token"

# Home Assistant 地址 (内网地址,用于 ML 容器访问)
HA_INTERNAL_HOST = "http://192.168.101.194:8123"

# 摄像头实体的 entity_picture 路径
# 例如: /api/camera_proxy/camera.bambu_lab_p1p_camera
CAMERA_ENTITY_PICTURE = "/api/camera_proxy/camera.h2d_0948db551900222_camera?token=9c530ad0cd8ca84aba3e3f6b1c71e10fdfacc39abb6e113e39119b825e436eef"

# 完整图片 URL (自动拼接,也可以直接填写完整 URL)
#IMAGE_URL = f"{HA_INTERNAL_HOST}{CAMERA_ENTITY_PICTURE}"
IMAGE_URL = f"https://makerworld.bblmw.cn/makerworld/model/CNe345bdace6c343/design/2025-08-18_778b7db48b21d.jpg"
# ================================================================


def test_obico_detection(image_url, obico_host=OBICO_HOST, auth_token=AUTH_TOKEN):
    """
    测试 Obico ML API 检测功能
    
    参数:
        image_url: 图片的完整 URL (例如: http://192.168.101.194:8123/api/camera_proxy/camera.xxx)
        obico_host: Obico ML API 服务器地址
        auth_token: 认证令牌
    """
    
    print("=" * 60)
    print("Obico ML API 检测测试")
    print("=" * 60)
    print(f"服务器地址: {obico_host}")
    print(f"认证令牌: {auth_token}")
    print(f"图片 URL: {image_url}")
    print("=" * 60)
    
    # 根据 Obico ML Server 源码,正确的 API 是 GET /p/?img=<image_url>
    api_url = f"{obico_host}/p/?img={image_url}"
    
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    
    print(f"\n正在发送请求到: {api_url}")
    
    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        
        print(f"\n响应状态码: {response.status_code}")
        print("\n" + "=" * 60)
        print("服务器返回内容:")
        print("=" * 60)
        
        # 尝试解析 JSON
        try:
            result = response.json()
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # 解析检测结果
            if "detections" in result:
                detections = result["detections"]
                print("\n" + "=" * 60)
                print("检测结果分析:")
                print("=" * 60)
                print(f"检测到的对象数量: {len(detections)}")
                
                # 计算 p_sum (所有检测置信度之和)
                p_sum = sum([det[1] for det in detections])
                print(f"置信度总和 (p_sum): {p_sum:.4f}")
                
                if detections:
                    print("\n详细检测信息:")
                    for i, detection in enumerate(detections, 1):
                        print(f"  对象 {i}: 类型={detection[0]}, 置信度={detection[1]:.4f}")
                
                # 判断是否可能有问题
                print("\n" + "=" * 60)
                if p_sum > 0.5:
                    print("⚠️  警告: 检测到较高的异常置信度,可能存在打印问题!")
                elif p_sum > 0.3:
                    print("⚡ 注意: 检测到中等异常置信度,需要关注")
                else:
                    print("✅ 正常: 异常置信度较低")
                print("=" * 60)
                
        except json.JSONDecodeError:
            print("(非 JSON 格式)")
            print(response.text)
        
        return response
        
    except requests.exceptions.Timeout:
        print("\n❌ 错误: 请求超时 (30秒)")
        return None
    except requests.exceptions.ConnectionError:
        print(f"\n❌ 错误: 无法连接到服务器 {obico_host}")
        print("请检查:")
        print("  1. 服务器地址是否正确")
        print("  2. 服务器是否正在运行")
        print("  3. 网络连接是否正常")
        return None
    except Exception as e:
        print(f"\n❌ 错误: {type(e).__name__}: {e}")
        return None


def main():
    """主函数"""
    # 使用文件开头配置的参数
    print("\n使用配置:")
    print(f"  Obico Host: {OBICO_HOST}")
    print(f"  Auth Token: {AUTH_TOKEN}")
    print(f"  Image URL: {IMAGE_URL}")
    print()
    
    # 执行测试
    test_obico_detection(IMAGE_URL)


if __name__ == "__main__":
    main()
