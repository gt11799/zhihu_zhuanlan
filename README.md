## 吴军老师的知乎专栏

> 之发明365合集

这个仓库已经改造成**纯静态站**版本：数据直接来自 `zhuanlan.db` 的 `wujun` 表，并导出到 `index.html`。

### 本地预览

直接打开 `index.html`，或使用：

```bash
python3 -m http.server 8000
```

然后访问 <http://localhost:8000>。

### 重新从 sqlite 导出静态页面

```bash
python3 tools/export_static_site.py
```

会重新生成：

- `index.html`
- `style.css`

### 发布到 GitHub Pages

1. 推送分支并合并到默认分支。
2. 在仓库 Settings → Pages 中选择 `Deploy from a branch`。
3. 选择默认分支（`/root`）后保存。
4. 等待部署完成后即可通过 GitHub Pages URL 访问。
