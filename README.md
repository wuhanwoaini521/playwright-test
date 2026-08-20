# 🎭 Playwright Test

> 基于 **Python Playwright** + **pytest + Page Object** 的企业级 **UI 自动化测试框架** 🚀
> 集成 **GitHub Actions** 多浏览器持续集成，一键产出 **Allure 报告**。

[![Playwright Tests](https://github.com/wuhanwoaini521/playwright-test/actions/workflows/playwright.yml/badge.svg)](https://github.com/wuhanwoaini521/playwright-test/actions)

---

## ✨ 框架特性

- 🏗️ **Page Object 模式**：`pages/` 页面对象 + `locators/` 元素定位 + `tests/` 用例三层分离
- 🌐 **多浏览器支持**：chromium / firefox / webkit，CI 中并行矩阵回归
- ⚙️ **多环境配置**：`PW_*` 环境变量覆盖，本地 / 测试 / 预发布 / 生产无缝切换
- 🔀 **并行执行**：pytest-xdist 自动并行，提速用例执行
- 🔁 **失败重试**：集成 pytest-rerunfailures，容忍偶发抖动
- 📊 **Allure 报告**：步骤化用例 + 失败自动截图
- 🔍 **失败留痕**：`--tracing=retain-on-failure` 记录完整浏览器操作轨迹
- 🚦 **CI/CD 就绪**：GitHub Actions 定时回归 + 缓存加速 + 产物归档

## 🛠️ 技术栈

| 技术 | 说明 | 版本 |
|------|------|------|
| 🐍 Python | 开发语言 | 3.9+ |
| 🎭 Playwright | 浏览器自动化 | >= 1.45 |
| 🧪 pytest | 测试框架 | >= 8.0 |
| 🔌 pytest-playwright | Playwright pytest 集成 | >= 0.5 |
| 🔀 pytest-xdist | 并发执行 | >= 3.5 |
| 🔁 pytest-rerunfailures | 失败重试 | >= 14.0 |
| 📊 allure-pytest | Allure 报告 | >= 2.13 |
| 🛡️ ruff | 代码规范 / lint | dev |

## 📁 项目结构

```
playwright-test/
├── .github/
│   └── workflows/
│       └── playwright.yml   # GitHub Actions：并发矩阵 + 定时回归 + 缓存
├── config/
│   ├── __init__.py
│   └── settings.py          # ⚙️ 全局配置（PW_* 环境变量覆盖）
├── locators/
│   ├── __init__.py
│   └── baidu_locators.py    # 📌 元素定位集中管理（入门示例）
├── pages/
│   ├── __init__.py
│   ├── base_page.py         # 🏠 页面基类：显式等待 / 日志 / 通用操作
│   └── search_page.py       # 📄 页面对象示例（百度搜索）
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # 🧩 全局 fixture（浏览器上下文 / 页面 / 失败截图）
│   ├── main.py              # 🚀 命令行入口（pw-test）
│   ├── markers.py           # 🔖 自定义 pytest 标记
│   └── test_baidu_search.py # 🧪 页面对象测试用例
├── utils/
│   ├── __init__.py
│   └── logger.py            # 📝 统一结构化日志
├── examples/
│   ├── test_example.py      # 📖 基础 pytest 示例
│   └── codegen_test.py      # 🎙️ playwright codegen 录制示例
├── pyproject.toml           # 📦 uv + pytest + ruff 配置
├── uv.lock                  # 🔒 uv 锁定的依赖版本
└── README.md
```

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/wuhanwoaini521/playwright-test.git
cd playwright-test

# 依赖管理统一使用 uv（自动创建 .venv）
uv sync
```

> 💡 依赖管理统一使用 **uv**，详见 [uv 官方文档](https://docs.astral.sh/uv/)。

### 安装浏览器

```bash
# 安装全部浏览器
uv run playwright install --with-deps

# 或只装用到的
uv run playwright install --with-deps chromium
```

### 运行测试

```bash
# 运行全部测试（自动并行 + Allure 输出）
uv run pytest

# 指定浏览器
uv run pytest --browser=firefox

# 只跑冒烟标记
uv run pytest -m smoke

# 串行执行（排查并发问题）
uv run pytest -n=0

# 只跑单个用例
uv run pytest tests/test_baidu_search.py::TestBaiduSearch::test_open_homepage
```

## ⚙️ 配置说明

所有配置项均可通过环境变量覆盖（`PW_` 前缀）：

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| `PW_BASE_URL` | `https://www.baidu.com` | 被测环境基础地址 |
| `PW_HEADLESS` | `true` | 是否无头模式 |
| `PW_TIMEOUT` | `30000` | 全局超时（毫秒） |
| `PW_VIEWPORT_WIDTH` | `1920` | 浏览器视口宽度 |
| `PW_VIEWPORT_HEIGHT` | `1080` | 浏览器视口高度 |
| `PW_RETRIES` | `0` | 失败重试次数 |
| `PW_TRACING` | `retain-on-failure` | trace 录制模式 |

示例：

```bash
PW_BASE_URL=https://example.com PW_HEADLESS=false uv run pytest
```

## 🏗️ 架构分层

```
  tests/  (测试用例：断言业务结果)
     │
  pages/  (页面对象：封装页面操作与业务方法)
     │
locators/ (元素定位：集中管理定位符，页面只做操作)
     │
config/  (全局配置)  +  utils/  (通用工具)
```

- **config/settings.py** — 全局不可变配置，支持环境变量覆盖。
- **pages/base_page.py** — 页面抽象基类：统一超时、日志、显式等待、通用操作与断言。
- **locators/** — 元素定位与页面对象分离，改定位不改业务。
- **tests/conftest.py** — 全局 fixture：浏览器上下文、每用例页面、失败自动截图进 Allure。

## 📊 Allure 报告

```bash
# 生成并打开报告
uv run allure generate allure-results -o allure-report --clean
uv run allure open allure-report
```

## 🚦 GitHub Actions

CI 支持 **push / PR / 每日定时回归 / 手动触发**：

- 🌐 三浏览器并行矩阵（chromium / firefox / webkit）
- 💾 uv 依赖 + Playwright 浏览器缓存，加速构建
- 📤 失败产物（trace / 截图）与 Allure 结果自动归档
- 🔀 并发控制，避免重复构建撞车

## 📝 如何新增一个用例

1. 📌 在 `locators/` 新增定位符类
2. 📄 在 `pages/` 新建页面对象（继承 `BasePage`）
3. 🧪 在 `tests/` 新增测试类与方法
4. 🚦 提交 push，CI 自动执行多浏览器回归

## 📄 License

MIT License © 2024 [wuhanwoaini521](https://github.com/wuhanwoaini521)
