"""
CommitPilot Internationalization (i18n) Module
Supports multiple languages for user interface
"""

from typing import Dict

# Supported languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "zh": "简体中文",
    "zh-tw": "繁體中文",
    "ja": "日本語",
    "ko": "한국어",
    "es": "Español",
}

# Current language
_current_language = "en"

# Message translations
MESSAGES: Dict[str, Dict[str, str]] = {
    "en": {
        # Errors
        "error.not_git_repo": "Not a Git repository",
        "error.no_staged_changes": "No staged changes found",
        "error.commit_failed": "Commit failed",
        
        # Hints
        "hint.stage_files": "Use 'git add <files>' to stage your changes first",
        
        # Generate
        "generated_message": "Generated Commit Message:",
        "confidence": "Confidence",
        "alternatives": "Alternative suggestions",
        
        # Commit
        "committing": "Committing changes",
        "commit_success": "Commit created successfully!",
        "dry_run": "Dry run - would commit with message",
        "edit_hint": "Edit the message above. Lines starting with # will be ignored.",
        
        # Analyze
        "analysis_result": "Change Analysis",
        "files_changed": "Files changed",
        "additions": "Additions",
        "deletions": "Deletions",
        "new_files": "New files",
        "modified_files": "Modified files",
        "deleted_files": "Deleted files",
        "breaking_change_detected": "Breaking change detected",
        "suggested_type": "Suggested type",
        "suggested_scope": "Suggested scope",
        
        # Hook
        "hook_installed": "Git hook installed successfully",
        "hook_uninstalled": "Git hook uninstalled",
        "hook_not_found": "No CommitPilot hook found",
    },
    "zh": {
        # Errors
        "error.not_git_repo": "不是Git仓库",
        "error.no_staged_changes": "没有找到暂存的更改",
        "error.commit_failed": "提交失败",
        
        # Hints
        "hint.stage_files": "请先使用 'git add <files>' 暂存您的更改",
        
        # Generate
        "generated_message": "生成的提交信息：",
        "confidence": "置信度",
        "alternatives": "备选建议",
        
        # Commit
        "committing": "正在提交更改",
        "commit_success": "提交成功！",
        "dry_run": "预览模式 - 将使用以下信息提交",
        "edit_hint": "编辑上方信息。以 # 开头的行将被忽略。",
        
        # Analyze
        "analysis_result": "更改分析",
        "files_changed": "更改文件数",
        "additions": "新增行数",
        "deletions": "删除行数",
        "new_files": "新文件",
        "modified_files": "修改的文件",
        "deleted_files": "删除的文件",
        "breaking_change_detected": "检测到破坏性更改",
        "suggested_type": "建议类型",
        "suggested_scope": "建议范围",
        
        # Hook
        "hook_installed": "Git钩子安装成功",
        "hook_uninstalled": "Git钩子已卸载",
        "hook_not_found": "未找到CommitPilot钩子",
    },
    "zh-tw": {
        # Errors
        "error.not_git_repo": "不是Git儲存庫",
        "error.no_staged_changes": "沒有找到暫存的變更",
        "error.commit_failed": "提交失敗",
        
        # Hints
        "hint.stage_files": "請先使用 'git add <files>' 暫存您的變更",
        
        # Generate
        "generated_message": "產生的提交訊息：",
        "confidence": "信心度",
        "alternatives": "備選建議",
        
        # Commit
        "committing": "正在提交變更",
        "commit_success": "提交成功！",
        "dry_run": "預覽模式 - 將使用以下訊息提交",
        "edit_hint": "編輯上方訊息。以 # 開頭的行將被忽略。",
        
        # Analyze
        "analysis_result": "變更分析",
        "files_changed": "變更檔案數",
        "additions": "新增行數",
        "deletions": "刪除行數",
        "new_files": "新檔案",
        "modified_files": "修改的檔案",
        "deleted_files": "刪除的檔案",
        "breaking_change_detected": "偵測到破壞性變更",
        "suggested_type": "建議類型",
        "suggested_scope": "建議範圍",
        
        # Hook
        "hook_installed": "Git鉤子安裝成功",
        "hook_uninstalled": "Git鉤子已卸載",
        "hook_not_found": "未找到CommitPilot鉤子",
    },
    "ja": {
        # Errors
        "error.not_git_repo": "Gitリポジトリではありません",
        "error.no_staged_changes": "ステージされた変更が見つかりません",
        "error.commit_failed": "コミットに失敗しました",
        
        # Hints
        "hint.stage_files": "まず 'git add <files>' で変更をステージしてください",
        
        # Generate
        "generated_message": "生成されたコミットメッセージ：",
        "confidence": "信頼度",
        "alternatives": "代替案",
        
        # Commit
        "committing": "変更をコミット中",
        "commit_success": "コミット成功！",
        "dry_run": "ドライラン - 以下のメッセージでコミットします",
        "edit_hint": "上記のメッセージを編集してください。#で始まる行は無視されます。",
        
        # Analyze
        "analysis_result": "変更分析",
        "files_changed": "変更ファイル数",
        "additions": "追加行数",
        "deletions": "削除行数",
        "new_files": "新規ファイル",
        "modified_files": "変更されたファイル",
        "deleted_files": "削除されたファイル",
        "breaking_change_detected": "破壊的変更が検出されました",
        "suggested_type": "推奨タイプ",
        "suggested_scope": "推奨スコープ",
        
        # Hook
        "hook_installed": "Gitフックがインストールされました",
        "hook_uninstalled": "Gitフックがアンインストールされました",
        "hook_not_found": "CommitPilotフックが見つかりません",
    },
    "ko": {
        # Errors
        "error.not_git_repo": "Git 저장소가 아닙니다",
        "error.no_staged_changes": "스테이징된 변경 사항이 없습니다",
        "error.commit_failed": "커밋 실패",
        
        # Hints
        "hint.stage_files": "'git add <files>'로 먼저 변경 사항을 스테이징하세요",
        
        # Generate
        "generated_message": "생성된 커밋 메시지:",
        "confidence": "신뢰도",
        "alternatives": "대안 제안",
        
        # Commit
        "committing": "변경 사항 커밋 중",
        "commit_success": "커밋 성공!",
        "dry_run": "드라이런 - 다음 메시지로 커밋합니다",
        "edit_hint": "위 메시지를 편집하세요. #으로 시작하는 줄은 무시됩니다.",
        
        # Analyze
        "analysis_result": "변경 분석",
        "files_changed": "변경된 파일 수",
        "additions": "추가된 줄",
        "deletions": "삭제된 줄",
        "new_files": "새 파일",
        "modified_files": "수정된 파일",
        "deleted_files": "삭제된 파일",
        "breaking_change_detected": "파괴적 변경 감지됨",
        "suggested_type": "제안된 유형",
        "suggested_scope": "제안된 범위",
        
        # Hook
        "hook_installed": "Git 훅이 설치되었습니다",
        "hook_uninstalled": "Git 훅이 제거되었습니다",
        "hook_not_found": "CommitPilot 훅을 찾을 수 없습니다",
    },
    "es": {
        # Errors
        "error.not_git_repo": "No es un repositorio Git",
        "error.no_staged_changes": "No se encontraron cambios preparados",
        "error.commit_failed": "Error al confirmar",
        
        # Hints
        "hint.stage_files": "Usa 'git add <archivos>' para preparar tus cambios primero",
        
        # Generate
        "generated_message": "Mensaje de confirmación generado:",
        "confidence": "Confianza",
        "alternatives": "Sugerencias alternativas",
        
        # Commit
        "committing": "Confirmando cambios",
        "commit_success": "¡Confirmación creada con éxito!",
        "dry_run": "Simulación - confirmaría con el mensaje",
        "edit_hint": "Edita el mensaje arriba. Las líneas que empiezan con # se ignorarán.",
        
        # Analyze
        "analysis_result": "Análisis de cambios",
        "files_changed": "Archivos modificados",
        "additions": "Adiciones",
        "deletions": "Eliminaciones",
        "new_files": "Archivos nuevos",
        "modified_files": "Archivos modificados",
        "deleted_files": "Archivos eliminados",
        "breaking_change_detected": "Cambio importante detectado",
        "suggested_type": "Tipo sugerido",
        "suggested_scope": "Ámbito sugerido",
        
        # Hook
        "hook_installed": "Git hook instalado con éxito",
        "hook_uninstalled": "Git hook desinstalado",
        "hook_not_found": "No se encontró el hook de CommitPilot",
    },
}


def set_language(lang: str) -> None:
    """Set the current language"""
    global _current_language
    if lang in SUPPORTED_LANGUAGES:
        _current_language = lang
    else:
        _current_language = "en"


def get_language() -> str:
    """Get the current language"""
    return _current_language


def get_message(key: str) -> str:
    """Get a message in the current language"""
    messages = MESSAGES.get(_current_language, MESSAGES["en"])
    return messages.get(key, MESSAGES["en"].get(key, key))


def get_all_messages(lang: str = None) -> Dict[str, str]:
    """Get all messages for a language"""
    language = lang or _current_language
    return MESSAGES.get(language, MESSAGES["en"]).copy()
