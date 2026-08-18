# 🎭 Playwright Test

> 基于 **Python Playwright** + **pytest** 的浏览器 UI 自动化测试示例 🚀
> 集成 **GitHub Actions** 持续集成，一键跑通浏览器自动化。

[![Playwright Tests](https://github.com/wuhanwoaini521/playwright-test/actions/workflows/playwright.yml/badge.svg)](https://github.com/wuhanwoaini521/playwright-test/actions)

---

## ✨ 项目特色

- 🧪 **pytest 原生支持**：借助 `pytest-playwright` 插件，fixture、参数化、报告应有尽有
- 🤖 **自动化录制**：附赠 `playwright codegen` 生成的交互脚本示例
- 🚦 **CI / CD 就绪**：GitHub Actions 自动安装浏览器并跑测试
- 🔍 **失败留痕**：测试失败时自动保存 tracing，方便排查

## 🛠️ 技术栈

| 技术 | 版本 |
|------|------|
| 🐍 Python | 3.12 |
| 🎭 Playwright | >= 1.45 |
| 🧪 pytest | >= 8.0 |
| 🔌 pytest-playwright | >= 0.5 |

## 📦 安装

```bash
# 克隆项目
git clone https://github.com/wuhanwoaini521/playwright-test.git
cd playwright-test

# 安装 pipenv 与依赖
pip install pipenv
pipenv install --dev

# 安装 Chromium 浏览器
pipenv run playwright install chromium
```

> 💡 不想用 pipenv？直接用 `pip install -r requirements.txt` 也可以。

## 🚀 运行测试

```bash
# 运行全部测试
pipenv run pytest --browser=chromium

# 运行并保留失败日志
pipenv run pytest --browser=chromium --tracing=retain-on-failure

# 只运行某个文件
pipenv run pytest test_example.py
```

## 📁 项目结构

```
playwright-test/
├── .github/
│   └── workflows/
│       └── playwright.yml   # GitHub Actions CI 配置
├── Pipfile                  # pipenv 依赖管理
├── requirements.txt         # pip 依赖清单
├── test_example.py          # pytest UI 测试示例
└── codegen_test.py          # codegen 录制的交互脚本
```

## 🧩 核心用法

### 📝 pytest 写测试

```python
def test_main_navigation(page):
    """验证访问百度首页后 URL 正确。"""
    expect(page).to_have_url("https://www.baidu.com/")
```

`pytest-playwright` 会自动注入 `page` fixture，超省心！

### 🎙️ 录制脚本

```bash
playwright codegen https://www.baidu.com
```

录制完生成的代码会直接打印出来，复制即用。

## 🚦 GitHub Actions

每次 push 或 PR 到 `main`/`master` 分支都会自动触发 CI：

1. 🔧 安装 Python 3.12
2. 📦 安装依赖 + Chromium
3. 🧪 运行全部 pytest 用例
4. 📤 失败时上传测试报告

## 📄 License

MIT License © 2024 [wuhanwoaini521](https://github.com/wuhanwoaini521)
