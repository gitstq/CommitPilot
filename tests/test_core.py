"""Tests for CommitPilot"""

import pytest
import os
import tempfile
import subprocess
from pathlib import Path

from commitpilot.core import (
    CommitAnalyzer,
    MessageGenerator,
    CommitType,
    ChangeScope,
    FileChange,
    DiffAnalysis,
    CommitStats,
)


class TestChangeScope:
    """Tests for ChangeScope detection"""
    
    def test_detect_api_scope(self):
        """Test API scope detection"""
        files = ["api/users.py", "api/routes.py"]
        assert ChangeScope.detect_scope(files) == "api"
    
    def test_detect_ui_scope(self):
        """Test UI scope detection"""
        files = ["components/Button.tsx", "views/Home.vue"]
        assert ChangeScope.detect_scope(files) == "ui"
    
    def test_detect_test_scope(self):
        """Test test scope detection"""
        files = ["tests/test_core.py", "spec/feature_spec.rb"]
        assert ChangeScope.detect_scope(files) == "test"
    
    def test_no_scope(self):
        """Test when no clear scope"""
        files = ["main.py", "utils.py"]
        assert ChangeScope.detect_scope(files) is None


class TestFileChange:
    """Tests for FileChange dataclass"""
    
    def test_extension_detection(self):
        """Test file extension detection"""
        change = FileChange(path="src/main.py", status="M")
        assert change.extension == ".py"
    
    def test_binary_detection(self):
        """Test binary file detection"""
        change = FileChange(path="images/logo.png", status="A")
        assert change.is_binary
    
    def test_text_file_not_binary(self):
        """Test text file is not binary"""
        change = FileChange(path="src/main.py", status="M")
        assert not change.is_binary


class TestDiffAnalysis:
    """Tests for DiffAnalysis"""
    
    def test_total_changes(self):
        """Test total changes calculation"""
        analysis = DiffAnalysis(
            total_additions=100,
            total_deletions=50
        )
        assert analysis.total_changes == 150
    
    def test_file_count(self):
        """Test file count"""
        analysis = DiffAnalysis(files=[
            FileChange("a.py", "M"),
            FileChange("b.py", "A"),
        ])
        assert analysis.file_count == 2


class TestCommitAnalyzer:
    """Tests for CommitAnalyzer"""
    
    def test_detect_type_docs(self):
        """Test documentation type detection"""
        analyzer = CommitAnalyzer()
        analysis = DiffAnalysis(files=[
            FileChange("README.md", "M"),
            FileChange("docs/guide.md", "M"),
        ])
        assert analyzer.detect_type(analysis) == CommitType.DOCS
    
    def test_detect_type_test(self):
        """Test test type detection"""
        analyzer = CommitAnalyzer()
        analysis = DiffAnalysis(files=[
            FileChange("tests/test_main.py", "M"),
            FileChange("tests/test_utils.py", "M"),
        ])
        assert analyzer.detect_type(analysis) == CommitType.TEST
    
    def test_detect_type_feat(self):
        """Test feature type detection for new files"""
        analyzer = CommitAnalyzer()
        analysis = DiffAnalysis(
            files=[FileChange("new_feature.py", "A")],
            new_files=["new_feature.py"]
        )
        assert analyzer.detect_type(analysis) == CommitType.FEAT
    
    def test_generate_subject(self):
        """Test subject generation"""
        analyzer = CommitAnalyzer()
        analysis = DiffAnalysis(files=[
            FileChange("src/main.py", "M"),
        ])
        subject = analyzer.generate_subject(analysis, CommitType.FIX)
        assert "main.py" in subject


class TestMessageGenerator:
    """Tests for MessageGenerator"""
    
    def test_conventional_format(self):
        """Test conventional commit format"""
        from commitpilot.core import CommitSuggestion
        
        suggestion = CommitSuggestion(
            type=CommitType.FEAT,
            scope="api",
            subject="add new endpoint",
            breaking=False
        )
        
        message = suggestion.to_message("conventional")
        assert message.startswith("feat(api):")
        assert "add new endpoint" in message
    
    def test_gitmoji_format(self):
        """Test GitMoji format"""
        from commitpilot.core import CommitSuggestion
        
        suggestion = CommitSuggestion(
            type=CommitType.FEAT,
            scope=None,
            subject="add new feature",
            breaking=False
        )
        
        message = suggestion.to_message("gitmoji")
        assert "✨" in message
    
    def test_breaking_change(self):
        """Test breaking change format"""
        from commitpilot.core import CommitSuggestion
        
        suggestion = CommitSuggestion(
            type=CommitType.FEAT,
            scope="api",
            subject="remove deprecated endpoint",
            breaking=True
        )
        
        message = suggestion.to_message("conventional")
        assert "!" in message
        assert "BREAKING CHANGE" in message


class TestCommitStats:
    """Tests for CommitStats"""
    
    def test_format_stats(self):
        """Test stats formatting"""
        stats = {
            "period_days": 30,
            "total_commits": 100,
            "authors": {"Alice": 60, "Bob": 40},
            "types": {"feat": 50, "fix": 30, "docs": 20},
            "avg_per_day": 3.33
        }
        
        output = CommitStats.format_stats(stats)
        assert "100" in output
        assert "feat" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
