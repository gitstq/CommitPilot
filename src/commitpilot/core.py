"""
CommitPilot Core Module - Git Commit Analysis and Message Generation
"""

import os
import re
import subprocess
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path
from datetime import datetime


class CommitType(Enum):
    """Standard commit types following Conventional Commits specification"""
    FEAT = "feat"       # New feature
    FIX = "fix"         # Bug fix
    DOCS = "docs"       # Documentation changes
    STYLE = "style"     # Code style changes (formatting, semicolons, etc)
    REFACTOR = "refactor"  # Code refactoring
    PERF = "perf"       # Performance improvements
    TEST = "test"       # Adding or updating tests
    BUILD = "build"     # Build system or dependency changes
    CI = "ci"           # CI/CD configuration changes
    CHORE = "chore"     # Other changes that don't modify src or test files
    REVERT = "revert"   # Reverts a previous commit


class ChangeScope:
    """Analyze the scope of changes"""
    
    @staticmethod
    def detect_scope(files: List[str]) -> Optional[str]:
        """Detect the scope based on changed files"""
        if not files:
            return None
        
        # Common scope patterns
        scope_patterns = {
            "api": ["api/", "routes/", "controllers/", "endpoints/"],
            "ui": ["components/", "views/", "pages/", "styles/", "css/"],
            "core": ["core/", "lib/", "src/core/"],
            "config": ["config/", "settings/", ".env", "config."],
            "db": ["db/", "migrations/", "models/", "schema/"],
            "auth": ["auth/", "login/", "user/", "permission/"],
            "test": ["tests/", "test/", "__tests__/", "spec/"],
            "docs": ["docs/", "README", "CHANGELOG", ".md"],
            "cli": ["cli/", "commands/", "bin/"],
            "utils": ["utils/", "helpers/", "common/"],
        }
        
        for scope, patterns in scope_patterns.items():
            for file in files:
                for pattern in patterns:
                    if pattern in file.lower():
                        return scope
        
        return None


@dataclass
class FileChange:
    """Represents a single file change"""
    path: str
    status: str  # A=Added, M=Modified, D=Deleted, R=Renamed
    additions: int = 0
    deletions: int = 0
    
    @property
    def extension(self) -> str:
        """Get file extension"""
        return Path(self.path).suffix.lower()
    
    @property
    def is_binary(self) -> bool:
        """Check if file is binary"""
        binary_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', 
                           '.zip', '.tar', '.gz', '.so', '.dll', '.exe'}
        return self.extension in binary_extensions


@dataclass
class DiffAnalysis:
    """Analysis result of git diff"""
    files: List[FileChange] = field(default_factory=list)
    total_additions: int = 0
    total_deletions: int = 0
    has_breaking_change: bool = False
    new_files: List[str] = field(default_factory=list)
    deleted_files: List[str] = field(default_factory=list)
    modified_files: List[str] = field(default_factory=list)
    
    @property
    def total_changes(self) -> int:
        return self.total_additions + self.total_deletions
    
    @property
    def file_count(self) -> int:
        return len(self.files)


@dataclass
class CommitSuggestion:
    """A commit message suggestion"""
    type: CommitType
    scope: Optional[str]
    subject: str
    body: Optional[str] = None
    footer: Optional[str] = None
    breaking: bool = False
    confidence: float = 0.0
    
    def to_message(self, style: str = "conventional") -> str:
        """Convert to commit message string"""
        if style == "gitmoji":
            return self._to_gitmoji()
        elif style == "angular":
            return self._to_angular()
        else:
            return self._to_conventional()
    
    def _to_conventional(self) -> str:
        """Generate conventional commit message"""
        prefix = f"{self.type.value}"
        if self.scope:
            prefix += f"({self.scope})"
        if self.breaking:
            prefix += "!"
        
        message = f"{prefix}: {self.subject}"
        
        if self.body:
            message += f"\n\n{self.body}"
        
        if self.footer:
            message += f"\n\n{self.footer}"
        elif self.breaking:
            message += "\n\nBREAKING CHANGE: This commit introduces breaking changes."
        
        return message
    
    def _to_angular(self) -> str:
        """Generate Angular-style commit message"""
        return self._to_conventional()
    
    def _to_gitmoji(self) -> str:
        """Generate GitMoji-style commit message"""
        emoji_map = {
            CommitType.FEAT: "✨",
            CommitType.FIX: "🐛",
            CommitType.DOCS: "📝",
            CommitType.STYLE: "💄",
            CommitType.REFACTOR: "♻️",
            CommitType.PERF: "⚡",
            CommitType.TEST: "✅",
            CommitType.BUILD: "📦",
            CommitType.CI: "👷",
            CommitType.CHORE: "🔧",
            CommitType.REVERT: "⏪",
        }
        
        emoji = emoji_map.get(self.type, "📝")
        scope_str = f"({self.scope})" if self.scope else ""
        breaking_emoji = "💥" if self.breaking else ""
        
        message = f"{emoji} {breaking_emoji}{scope_str} {self.subject}"
        
        if self.body:
            message += f"\n\n{self.body}"
        
        return message


class GitCommand:
    """Execute Git commands safely"""
    
    @staticmethod
    def run(args: List[str], cwd: Optional[str] = None) -> Tuple[bool, str]:
        """Run a git command and return success status and output"""
        try:
            result = subprocess.run(
                ["git"] + args,
                capture_output=True,
                text=True,
                cwd=cwd or os.getcwd(),
                timeout=30
            )
            return result.returncode == 0, result.stdout.strip()
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except FileNotFoundError:
            return False, "Git not found"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def is_git_repo() -> bool:
        """Check if current directory is a git repository"""
        success, _ = GitCommand.run(["rev-parse", "--is-inside-work-tree"])
        return success
    
    @staticmethod
    def get_staged_files() -> List[str]:
        """Get list of staged files"""
        success, output = GitCommand.run(["diff", "--cached", "--name-only"])
        return output.split("\n") if success and output else []
    
    @staticmethod
    def get_unstaged_files() -> List[str]:
        """Get list of unstaged modified files"""
        success, output = GitCommand.run(["diff", "--name-only"])
        return output.split("\n") if success and output else []
    
    @staticmethod
    def get_untracked_files() -> List[str]:
        """Get list of untracked files"""
        success, output = GitCommand.run(["ls-files", "--others", "--exclude-standard"])
        return output.split("\n") if success and output else []
    
    @staticmethod
    def get_diff_stats() -> Dict[str, Any]:
        """Get diff statistics"""
        success, output = GitCommand.run([
            "diff", "--cached", "--numstat"
        ])
        
        stats = {"additions": 0, "deletions": 0, "files": []}
        if success and output:
            for line in output.split("\n"):
                if line.strip():
                    parts = line.split("\t")
                    if len(parts) >= 3:
                        add = int(parts[0]) if parts[0] != "-" else 0
                        delete = int(parts[1]) if parts[1] != "-" else 0
                        stats["additions"] += add
                        stats["deletions"] += delete
                        stats["files"].append({
                            "path": parts[2],
                            "additions": add,
                            "deletions": delete
                        })
        
        return stats
    
    @staticmethod
    def get_diff_content() -> str:
        """Get the actual diff content for analysis"""
        success, output = GitCommand.run(["diff", "--cached"])
        return output if success else ""
    
    @staticmethod
    def get_recent_commits(count: int = 10) -> List[Dict[str, str]]:
        """Get recent commit history"""
        success, output = GitCommand.run([
            "log", f"-{count}", "--pretty=format:%H|%s|%an|%ad",
            "--date=short"
        ])
        
        commits = []
        if success and output:
            for line in output.split("\n"):
                if line.strip():
                    parts = line.split("|")
                    if len(parts) >= 4:
                        commits.append({
                            "hash": parts[0][:7],
                            "subject": parts[1],
                            "author": parts[2],
                            "date": parts[3]
                        })
        
        return commits
    
    @staticmethod
    def commit(message: str) -> Tuple[bool, str]:
        """Create a commit with the given message"""
        return GitCommand.run(["commit", "-m", message])


class CommitAnalyzer:
    """Analyze Git changes and generate commit suggestions"""
    
    # Patterns for detecting change types
    TYPE_PATTERNS = {
        CommitType.FEAT: [
            r"new\s+(feature|function|method|class|module)",
            r"add\s+(support|ability|feature)",
            r"implement\s+new",
            r"introduce\s+new",
        ],
        CommitType.FIX: [
            r"fix\s+(bug|issue|error|problem)",
            r"resolve\s+(bug|issue)",
            r"correct\s+(error|mistake)",
            r"patch\s+",
        ],
        CommitType.DOCS: [
            r"update\s+(readme|documentation|docs)",
            r"add\s+(documentation|docs)",
            r"improve\s+docs",
        ],
        CommitType.REFACTOR: [
            r"refactor\s+",
            r"restructure\s+",
            r"reorganize\s+",
            r"simplify\s+",
        ],
        CommitType.PERF: [
            r"optimize\s+",
            r"improve\s+performance",
            r"speed\s+up",
            r"reduce\s+(memory|time)",
        ],
        CommitType.TEST: [
            r"add\s+(test|tests|spec)",
            r"update\s+test",
            r"fix\s+test",
        ],
        CommitType.STYLE: [
            r"format\s+",
            r"style\s+",
            r"lint\s+",
        ],
    }
    
    # Breaking change indicators
    BREAKING_PATTERNS = [
        r"breaking\s+change",
        r"remove\s+(public|exported|api)",
        r"deprecate\s+",
        r"rename\s+(class|function|method|module)",
        r"change\s+(signature|interface|api)",
    ]
    
    def __init__(self, repo_path: Optional[str] = None):
        """Initialize the analyzer"""
        self.repo_path = repo_path or os.getcwd()
    
    def analyze(self) -> DiffAnalysis:
        """Analyze current staged changes"""
        analysis = DiffAnalysis()
        
        if not GitCommand.is_git_repo():
            return analysis
        
        # Get diff stats
        stats = GitCommand.get_diff_stats()
        analysis.total_additions = stats["additions"]
        analysis.total_deletions = stats["deletions"]
        
        # Analyze each file
        for file_info in stats["files"]:
            change = FileChange(
                path=file_info["path"],
                status=self._get_file_status(file_info["path"]),
                additions=file_info["additions"],
                deletions=file_info["deletions"]
            )
            analysis.files.append(change)
            
            if change.status == "A":
                analysis.new_files.append(change.path)
            elif change.status == "D":
                analysis.deleted_files.append(change.path)
            else:
                analysis.modified_files.append(change.path)
        
        # Check for breaking changes in diff content
        diff_content = GitCommand.get_diff_content()
        analysis.has_breaking_change = self._detect_breaking_change(diff_content)
        
        return analysis
    
    def _get_file_status(self, path: str) -> str:
        """Get the status of a file (A/M/D/R)"""
        success, output = GitCommand.run(["diff", "--cached", "--name-status"])
        if success and output:
            for line in output.split("\n"):
                if line.strip() and path in line:
                    return line[0]
        return "M"  # Default to modified
    
    def _detect_breaking_change(self, diff_content: str) -> bool:
        """Detect if the changes include breaking changes"""
        diff_lower = diff_content.lower()
        for pattern in self.BREAKING_PATTERNS:
            if re.search(pattern, diff_lower):
                return True
        
        # Check for removed exported functions/classes
        if re.search(r"^-\s*(export|public)\s+", diff_content, re.MULTILINE):
            return True
        
        return False
    
    def detect_type(self, analysis: DiffAnalysis) -> CommitType:
        """Detect the commit type based on changes"""
        if not analysis.files:
            return CommitType.CHORE
        
        # Check file extensions and paths
        extensions = {f.extension for f in analysis.files}
        paths = [f.path.lower() for f in analysis.files]
        
        # Documentation changes
        if all(f.extension in {'.md', '.txt', '.rst'} or 'doc' in f.path.lower() 
               for f in analysis.files):
            return CommitType.DOCS
        
        # Test changes
        if all('test' in p or 'spec' in p or '__test__' in p for p in paths):
            return CommitType.TEST
        
        # New files (feature)
        if analysis.new_files and not analysis.modified_files and not analysis.deleted_files:
            return CommitType.FEAT
        
        # Only deletions
        if analysis.deleted_files and not analysis.new_files and not analysis.modified_files:
            # Could be refactor (cleanup) or fix
            return CommitType.REFACTOR
        
        # Check for config/build files
        config_extensions = {'.json', '.yaml', '.yml', '.toml', '.ini', '.cfg'}
        if extensions.issubset(config_extensions):
            return CommitType.CHORE
        
        # Default to feat for new features, fix for modifications
        if analysis.new_files:
            return CommitType.FEAT
        
        return CommitType.FIX
    
    def generate_subject(self, analysis: DiffAnalysis, commit_type: CommitType) -> str:
        """Generate a commit subject line"""
        if not analysis.files:
            return "update repository"
        
        # Get primary file or directory
        primary = analysis.files[0].path
        if len(analysis.files) > 1:
            # Use common directory
            parts = primary.split("/")
            if len(parts) > 1:
                primary = parts[0]
        
        # Generate action verb
        action_map = {
            CommitType.FEAT: "add",
            CommitType.FIX: "fix",
            CommitType.DOCS: "update",
            CommitType.STYLE: "format",
            CommitType.REFACTOR: "refactor",
            CommitType.PERF: "optimize",
            CommitType.TEST: "add tests for",
            CommitType.BUILD: "update build for",
            CommitType.CI: "update CI for",
            CommitType.CHORE: "update",
            CommitType.REVERT: "revert changes in",
        }
        
        action = action_map.get(commit_type, "update")
        
        # Clean up the subject
        subject = f"{action} {primary}"
        
        # Add context for multiple files
        if analysis.file_count > 1:
            subject += f" and {analysis.file_count - 1} other files"
        
        return subject


class MessageGenerator:
    """Generate commit messages with various styles"""
    
    def __init__(self, style: str = "conventional"):
        """
        Initialize message generator.
        
        Args:
            style: Message style - 'conventional', 'angular', or 'gitmoji'
        """
        self.style = style
        self.analyzer = CommitAnalyzer()
    
    def generate(self, custom_type: Optional[str] = None,
                 scope: Optional[str] = None,
                 subject: Optional[str] = None,
                 body: Optional[str] = None) -> CommitSuggestion:
        """
        Generate a commit message suggestion.
        
        Args:
            custom_type: Override detected commit type
            scope: Custom scope
            subject: Custom subject line
            body: Commit body text
        """
        # Analyze changes
        analysis = self.analyzer.analyze()
        
        # Determine commit type
        if custom_type:
            try:
                commit_type = CommitType(custom_type.lower())
            except ValueError:
                commit_type = self.analyzer.detect_type(analysis)
        else:
            commit_type = self.analyzer.detect_type(analysis)
        
        # Determine scope
        if not scope:
            scope = ChangeScope.detect_scope([f.path for f in analysis.files])
        
        # Generate subject
        if not subject:
            subject = self.analyzer.generate_subject(analysis, commit_type)
        
        # Calculate confidence based on analysis quality
        confidence = self._calculate_confidence(analysis)
        
        return CommitSuggestion(
            type=commit_type,
            scope=scope,
            subject=subject,
            body=body,
            breaking=analysis.has_breaking_change,
            confidence=confidence
        )
    
    def _calculate_confidence(self, analysis: DiffAnalysis) -> float:
        """Calculate confidence score for the suggestion"""
        if not analysis.files:
            return 0.0
        
        score = 0.5  # Base score
        
        # More files = more confidence in type detection
        score += min(analysis.file_count * 0.05, 0.2)
        
        # More changes = more confidence
        if analysis.total_changes > 100:
            score += 0.1
        if analysis.total_changes > 500:
            score += 0.1
        
        # Clear scope detection
        if ChangeScope.detect_scope([f.path for f in analysis.files]):
            score += 0.1
        
        return min(score, 1.0)
    
    def generate_alternatives(self, count: int = 3) -> List[CommitSuggestion]:
        """Generate multiple alternative commit messages"""
        analysis = self.analyzer.analyze()
        
        alternatives = []
        
        # Primary suggestion
        primary = self.generate()
        alternatives.append(primary)
        
        # Alternative types based on analysis
        if primary.type != CommitType.FEAT and analysis.new_files:
            alt = self.generate(custom_type="feat")
            alt.confidence *= 0.8
            alternatives.append(alt)
        
        if primary.type != CommitType.REFACTOR and analysis.total_deletions > analysis.total_additions:
            alt = self.generate(custom_type="refactor")
            alt.confidence *= 0.7
            alternatives.append(alt)
        
        return alternatives[:count]


class CommitStats:
    """Analyze commit history statistics"""
    
    @staticmethod
    def get_stats(days: int = 30) -> Dict[str, Any]:
        """Get commit statistics for the last N days"""
        since = f"--since={days}.days.ago"
        
        # Total commits
        success, output = GitCommand.run([
            "log", since, "--oneline"
        ])
        total_commits = len(output.split("\n")) if success and output else 0
        
        # Commits by author
        success, output = GitCommand.run([
            "log", since, "--pretty=format:%an"
        ])
        authors = {}
        if success and output:
            for author in output.split("\n"):
                authors[author] = authors.get(author, 0) + 1
        
        # Commits by type (from conventional commits)
        success, output = GitCommand.run([
            "log", since, "--pretty=format:%s"
        ])
        types = {}
        if success and output:
            for subject in output.split("\n"):
                match = re.match(r"^(\w+)(\(.+\))?!?:", subject)
                if match:
                    ctype = match.group(1)
                    types[ctype] = types.get(ctype, 0) + 1
        
        return {
            "period_days": days,
            "total_commits": total_commits,
            "authors": authors,
            "types": types,
            "avg_per_day": round(total_commits / days, 2) if days > 0 else 0
        }
    
    @staticmethod
    def format_stats(stats: Dict[str, Any]) -> str:
        """Format statistics for display"""
        lines = [
            f"📊 Commit Statistics (Last {stats['period_days']} days)",
            "=" * 50,
            f"Total Commits: {stats['total_commits']}",
            f"Average per Day: {stats['avg_per_day']}",
            "",
            "📈 Commit Types:",
        ]
        
        for ctype, count in sorted(stats["types"].items(), 
                                   key=lambda x: x[1], reverse=True)[:5]:
            lines.append(f"  {ctype}: {count}")
        
        lines.append("")
        lines.append("👥 Top Contributors:")
        
        for author, count in sorted(stats["authors"].items(),
                                    key=lambda x: x[1], reverse=True)[:3]:
            lines.append(f"  {author}: {count}")
        
        return "\n".join(lines)
