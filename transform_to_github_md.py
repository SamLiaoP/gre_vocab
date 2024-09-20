import os
import re
from pathlib import Path

# 設定要處理的資料夾路徑
folder_path = Path("./")  # 根目錄

# 建立一個字典來儲存所有檔案的名稱及其對應的路徑
file_paths = {}

# 遍歷資料夾中的所有 .md 檔案並記錄檔案名稱與路徑
for file_path in folder_path.rglob("*.md"):
    file_name = file_path.stem
    # 取得相對於根目錄的路徑，並將空白字元轉換為 %20
    relative_path = str(file_path.relative_to(folder_path)).replace(" ", "%20")
    file_paths[file_name] = relative_path

# 重新遍歷資料夾中的所有 .md 檔案來替換連結並新增標題
for file_path in folder_path.rglob("*.md"):
    file_name = file_path.stem
    
    # 讀取檔案內容
    with file_path.open("r", encoding="utf-8") as file:
        content = file.read()
    
    # 找到所有的 [[連結]] 並將其替換為正確的相對路徑
    def replace_link(match):
        link_name = match.group(1)
        if link_name in file_paths:
            # 使用相對路徑並替換空白字元為 %20
            return f"[{link_name}](/{file_paths[link_name]})"
        else:
            return match.group(0)  # 如果找不到對應的檔案，保持原樣

    updated_content = re.sub(r"\[\[(.*?)\]\]", replace_link, content)
    
    # 在檔案的開頭加上標題
    updated_content = f"# {file_name}\n\n" + updated_content
    
    # 將修改過的內容寫回檔案
    with file_path.open("w", encoding="utf-8") as file:
        file.write(updated_content)

print("已完成檔案連結與標題的更新。")
