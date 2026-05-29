"""
CommitPilot CLI - Command Line Interface
"""

import argparse
import sys
import os
from typing import Optional, List

from commitpilot.core import (
    CommitAnalyzer,
    MessageGenerator,
    CommitStats,
    GitCommand,
    CommitType
)
from commitpilot.i18n import get_message, set_language, SUPPORTED_LANGUAGES


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser"""
    parser = argparse.ArgumentParser(
        prog="commitpilot",
        description="🚀 CommitPilot - Intelligent Git Commit Assistant CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  commitpilot generate          Generate a commit message for staged changes
  commitpilot generate --style gitmoji   Use GitMoji style
  commitpilot commit            Generate and commit in one step
  commitpilot stats             Show commit statistics
  commitpilot analyze           Analyze current changes

For more information: https://github.com/gitstq/CommitPilot
        """
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    parser.add_argument(
        "-l", "--language",
        choices=list(SUPPORTED_LANGUAGES.keys()),
        default="en",
        help="Output language (default: en)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Generate command
    gen_parser = subparsers.add_parser(
        "generate", 
        aliases=["gen", "g"],
        help="Generate commit message for staged changes"
    )
    gen_parser.add_argument(
        "-s", "--style",
        choices=["conventional", "angular", "gitmoji"],
        default="conventional",
        help="Commit message style (default: conventional)"
    )
    gen_parser.add_argument(
        "-t", "--type",
        choices=[t.value for t in CommitType],
        help="Override detected commit type"
    )
    gen_parser.add_argument(
        "--scope",
        help="Set custom scope"
    )
    gen_parser.add_argument(
        "--subject",
        help="Set custom subject"
    )
    gen_parser.add_argument(
        "--body",
        help="Add commit body"
    )
    gen_parser.add_argument(
        "-a", "--alternatives",
        action="store_true",
        help="Show alternative suggestions"
    )
    gen_parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )
    
    # Commit command
    commit_parser = subparsers.add_parser(
        "commit",
        aliases=["c"],
        help="Generate message and commit"
    )
    commit_parser.add_argument(
        "-s", "--style",
        choices=["conventional", "angular", "gitmoji"],
        default="conventional",
        help="Commit message style"
    )
    commit_parser.add_argument(
        "-e", "--edit",
        action="store_true",
        help="Open editor to edit message before committing"
    )
    commit_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be committed without committing"
    )
    
    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze",
        aliases=["a"],
        help="Analyze current staged changes"
    )
    analyze_parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )
    
    # Stats command
    stats_parser = subparsers.add_parser(
        "stats",
        help="Show commit history statistics"
    )
    stats_parser.add_argument(
        "-d", "--days",
        type=int,
        default=30,
        help="Number of days to analyze (default: 30)"
    )
    
    # Hook command
    hook_parser = subparsers.add_parser(
        "hook",
        help="Manage Git hooks"
    )
    hook_parser.add_argument(
        "action",
        choices=["install", "uninstall"],
        help="Install or uninstall prepare-commit-msg hook"
    )
    
    return parser


def cmd_generate(args) -> int:
    """Handle generate command"""
    set_language(args.language)
    
    # Check if in git repo
    if not GitCommand.is_git_repo():
        print("❌ " + get_message("error.not_git_repo"), file=sys.stderr)
        return 1
    
    # Check for staged changes
    staged = GitCommand.get_staged_files()
    if not staged:
        print("⚠️  " + get_message("error.no_staged_changes"), file=sys.stderr)
        print("\n💡 " + get_message("hint.stage_files"))
        return 1
    
    # Generate message
    generator = MessageGenerator(style=args.style)
    suggestion = generator.generate(
        custom_type=args.type,
        scope=args.scope,
        subject=args.subject,
        body=args.body
    )
    
    if args.json:
        import json
        output = {
            "type": suggestion.type.value,
            "scope": suggestion.scope,
            "subject": suggestion.subject,
            "body": suggestion.body,
            "breaking": suggestion.breaking,
            "confidence": suggestion.confidence,
            "message": suggestion.to_message(args.style)
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print("\n📝 " + get_message("generated_message"))
        print("-" * 50)
        print(suggestion.to_message(args.style))
        print("-" * 50)
        print(f"\n🎯 {get_message('confidence')}: {suggestion.confidence:.0%}")
        
        if args.alternatives:
            print("\n🔄 " + get_message("alternatives") + ":")
            for i, alt in enumerate(generator.generate_alternatives(3)[1:], 2):
                print(f"\n  [{i}] {alt.to_message(args.style)}")
    
    return 0


def cmd_commit(args) -> int:
    """Handle commit command"""
    set_language(args.language)
    
    if not GitCommand.is_git_repo():
        print("❌ " + get_message("error.not_git_repo"), file=sys.stderr)
        return 1
    
    staged = GitCommand.get_staged_files()
    if not staged:
        print("⚠️  " + get_message("error.no_staged_changes"), file=sys.stderr)
        return 1
    
    # Generate message
    generator = MessageGenerator(style=args.style)
    suggestion = generator.generate()
    message = suggestion.to_message(args.style)
    
    if args.dry_run:
        print("🔍 " + get_message("dry_run") + ":")
        print("-" * 50)
        print(message)
        print("-" * 50)
        return 0
    
    if args.edit:
        # Open editor
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as f:
            f.write(message)
            f.write("\n\n# " + get_message("edit_hint") + "\n")
            temp_path = f.name
        
        editor = os.environ.get('EDITOR', 'nano')
        os.system(f"{editor} {temp_path}")
        
        with open(temp_path, 'r') as f:
            message = f.read().split('\n\n#')[0].strip()
        
        os.unlink(temp_path)
    
    # Commit
    print("\n📝 " + get_message("committing") + "...")
    success, output = GitCommand.commit(message)
    
    if success:
        print("✅ " + get_message("commit_success"))
        print(f"\n{message}")
    else:
        print("❌ " + get_message("commit_failed") + f": {output}", file=sys.stderr)
        return 1
    
    return 0


def cmd_analyze(args) -> int:
    """Handle analyze command"""
    set_language(args.language)
    
    if not GitCommand.is_git_repo():
        print("❌ " + get_message("error.not_git_repo"), file=sys.stderr)
        return 1
    
    analyzer = CommitAnalyzer()
    analysis = analyzer.analyze()
    
    if args.json:
        import json
        output = {
            "files": [
                {
                    "path": f.path,
                    "status": f.status,
                    "additions": f.additions,
                    "deletions": f.deletions
                }
                for f in analysis.files
            ],
            "total_additions": analysis.total_additions,
            "total_deletions": analysis.total_deletions,
            "has_breaking_change": analysis.has_breaking_change,
            "new_files": analysis.new_files,
            "deleted_files": analysis.deleted_files,
            "modified_files": analysis.modified_files
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print("\n📊 " + get_message("analysis_result"))
        print("=" * 50)
        
        print(f"\n📁 {get_message('files_changed')}: {analysis.file_count}")
        print(f"   ➕ {get_message('additions')}: {analysis.total_additions}")
        print(f"   ➖ {get_message('deletions')}: {analysis.total_deletions}")
        
        if analysis.new_files:
            print(f"\n🆕 {get_message('new_files')}:")
            for f in analysis.new_files[:5]:
                print(f"   • {f}")
            if len(analysis.new_files) > 5:
                print(f"   ... and {len(analysis.new_files) - 5} more")
        
        if analysis.modified_files:
            print(f"\n✏️  {get_message('modified_files')}:")
            for f in analysis.modified_files[:5]:
                print(f"   • {f}")
        
        if analysis.deleted_files:
            print(f"\n🗑️  {get_message('deleted_files')}:")
            for f in analysis.deleted_files[:5]:
                print(f"   • {f}")
        
        if analysis.has_breaking_change:
            print(f"\n⚠️  {get_message('breaking_change_detected')}!")
        
        # Detect type
        commit_type = analyzer.detect_type(analysis)
        scope = analyzer.detect_scope([f.path for f in analysis.files])
        print(f"\n🎯 {get_message('suggested_type')}: {commit_type.value}")
        if scope:
            print(f"📦 {get_message('suggested_scope')}: {scope}")
    
    return 0


def cmd_stats(args) -> int:
    """Handle stats command"""
    set_language(args.language)
    
    if not GitCommand.is_git_repo():
        print("❌ " + get_message("error.not_git_repo"), file=sys.stderr)
        return 1
    
    stats = CommitStats.get_stats(args.days)
    print(CommitStats.format_stats(stats))
    
    return 0


def cmd_hook(args) -> int:
    """Handle hook command"""
    set_language(args.language)
    
    if not GitCommand.is_git_repo():
        print("❌ " + get_message("error.not_git_repo"), file=sys.stderr)
        return 1
    
    hook_path = ".git/hooks/prepare-commit-msg"
    
    if args.action == "install":
        hook_content = '''#!/bin/sh
# CommitPilot prepare-commit-msg hook
COMMIT_MSG_FILE=$1
COMMIT_SOURCE=$2

if [ -z "$COMMIT_SOURCE" ]; then
    # Only generate for new commits, not amend or merge
    commitpilot generate --json 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data['message'])
" > "$COMMIT_MSG_FILE" 2>/dev/null
fi
'''
        with open(hook_path, 'w') as f:
            f.write(hook_content)
        os.chmod(hook_path, 0o755)
        print("✅ " + get_message("hook_installed"))
        
    elif args.action == "uninstall":
        if os.path.exists(hook_path):
            os.unlink(hook_path)
            print("✅ " + get_message("hook_uninstalled"))
        else:
            print("⚠️  " + get_message("hook_not_found"))
    
    return 0


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point"""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    if not parsed_args.command:
        parser.print_help()
        return 0
    
    commands = {
        "generate": cmd_generate,
        "gen": cmd_generate,
        "g": cmd_generate,
        "commit": cmd_commit,
        "c": cmd_commit,
        "analyze": cmd_analyze,
        "a": cmd_analyze,
        "stats": cmd_stats,
        "hook": cmd_hook,
    }
    
    handler = commands.get(parsed_args.command)
    if handler:
        return handler(parsed_args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
