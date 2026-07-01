import asyncio
from pyppeteer import launch

async def main():
    # 启动浏览器
    browser = await launch(headless=True)
    try:
        # 创建新页面
        page = await browser.newPage()
        # 设置页面视口大小
        await page.setViewport({'width': 1280, 'height': 800})
        # 打开豆瓣电影 Top250 页面
        await page.goto('https://movie.douban.com/top250', waitUntil='networkidle2')

        # 等待电影信息元素加载完成
        await page.waitForSelector('.item')

        # 提取电影名称和评分
        movie_info = await page.evaluate('''() => {
            const items = document.querySelectorAll('.item');
            const result = [];
            items.forEach(item => {
                const title = item.querySelector('.hd a span').textContent.trim();
                const rating = item.querySelector('.rating_num').textContent.trim();
                result.push({
                    title: title,
                    rating: rating
                });
            });
            return result;
        }''')

        # 打印电影信息
        for info in movie_info:
            print(f"电影名称: {info['title']}, 评分: {info['rating']}")

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 关闭浏览器
        await browser.close()

# 运行异步函数
asyncio.get_event_loop().run_until_complete(main())