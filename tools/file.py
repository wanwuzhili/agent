from pathlib import Path

from langchain.tools import tool


def safe_path(WORKSPACE, path):
    target = (WORKSPACE / path).resolve()

    if not target.is_relative_to(WORKSPACE):
        raise ValueError(
            "非法路径：只能访问 agent_workspace"
        )

    return target

@tool
def read_file(path):
    """打开文件并读取内容"""

    try:
        target = safe_path(path)

        if not target.exists():
            return {
                "error": f"文件不存在: {path}"
            }

        if not target.is_file():
            return {
                "error": f"不是普通文件: {path}"
            }

        content = target.read_text(
            encoding="utf-8"
        )

        return {
            "success": True,
            "path": path,
            "content": content
        }

    except Exception as e:
        return {
            "error": str(e)
        }


@tool
def write_file(path, content):
    """将指定内容写入文件"""

    try:
        target = safe_path(path)

        target.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        target.write_text(
            content,
            encoding="utf-8"
        )

        return {
            "success": True,
            "path": path,
            "message": "文件写入成功"
        }

    except Exception as e:
        return {
            "error": str(e)
        }
