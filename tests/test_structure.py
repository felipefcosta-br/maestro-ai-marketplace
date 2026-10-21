import glob
import json
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = os.path.join(ROOT, "maestro-ai")

AGENTS = ["researcher", "analyst", "implementer", "tester", "specialist", "architect", "reviewer"]
READ_ONLY = ["researcher", "analyst", "architect", "reviewer"]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_json(path):
    return json.loads(read(path))


def frontmatter(path):
    text = read(path)
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, "missing frontmatter: " + path
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip()
    return fields


def text_files():
    skip = {".git", "__pycache__", "tests", ".maestro-ai"}
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in skip]
        for name in files:
            if name.endswith((".md", ".json", ".py", ".yml")):
                yield os.path.join(base, name)


class TestMetadata(unittest.TestCase):
    def test_versions_in_sync(self):
        plugin = load_json(os.path.join(PLUGIN, ".claude-plugin", "plugin.json"))
        market = load_json(os.path.join(ROOT, ".claude-plugin", "marketplace.json"))
        self.assertEqual(plugin["version"], market["plugins"][0]["version"])
        self.assertEqual(plugin["name"], market["plugins"][0]["name"])

    def test_changelog_has_version(self):
        plugin = load_json(os.path.join(PLUGIN, ".claude-plugin", "plugin.json"))
        self.assertIn("[%s]" % plugin["version"], read(os.path.join(ROOT, "CHANGELOG.md")))

    def test_author(self):
        plugin = load_json(os.path.join(PLUGIN, ".claude-plugin", "plugin.json"))
        self.assertTrue(plugin.get("author", {}).get("name"))


class TestAgents(unittest.TestCase):
    def test_all_agents(self):
        files = sorted(os.path.basename(p)[:-3] for p in glob.glob(os.path.join(PLUGIN, "agents", "*.md")))
        self.assertEqual(files, sorted(AGENTS))
        for name in AGENTS:
            fm = frontmatter(os.path.join(PLUGIN, "agents", name + ".md"))
            self.assertEqual(fm.get("name"), name)
            self.assertTrue(fm.get("description"))
            self.assertIn(fm.get("model"), ("haiku", "sonnet", "opus"))
            self.assertTrue(fm.get("tools"))

    def test_architect_is_opus(self):
        self.assertEqual(frontmatter(os.path.join(PLUGIN, "agents", "architect.md"))["model"], "opus")

    def test_read_only_agents(self):
        for name in READ_ONLY:
            tools = [t.strip() for t in frontmatter(os.path.join(PLUGIN, "agents", name + ".md"))["tools"].split(",")]
            self.assertNotIn("Edit", tools, name)
            self.assertNotIn("Write", tools, name)

    def test_only_researcher_uses_web(self):
        for name in AGENTS:
            tools = frontmatter(os.path.join(PLUGIN, "agents", name + ".md"))["tools"]
            has_web = "WebSearch" in tools or "WebFetch" in tools
            self.assertEqual(has_web, name == "researcher", name)


class TestSkillCommandsHooks(unittest.TestCase):
    def test_skill(self):
        self.assertEqual(frontmatter(os.path.join(PLUGIN, "skills", "orchestration", "SKILL.md"))["name"], "orchestration")

    def test_commands_have_description(self):
        commands = glob.glob(os.path.join(PLUGIN, "commands", "*.md"))
        self.assertEqual(len(commands), 6)
        for c in commands:
            self.assertTrue(frontmatter(c).get("description"), c)

    def test_hook_scripts_exist(self):
        hooks = load_json(os.path.join(PLUGIN, "hooks", "hooks.json"))
        scripts = re.findall(r"hooks/([\w.-]+\.py)", json.dumps(hooks))
        self.assertEqual(len(scripts), 4)
        for s in scripts:
            self.assertTrue(os.path.isfile(os.path.join(PLUGIN, "hooks", s)), s)


class TestLanguageRule(unittest.TestCase):
    def test_language_rule_present(self):
        skill = read(os.path.join(PLUGIN, "skills", "orchestration", "SKILL.md"))
        self.assertIn("## 0. Language", skill)
        self.assertIn("ask once", skill)
        self.assertIn("Language:", read(os.path.join(PLUGIN, "templates", "AGENTS.md")))
        self.assertIn("Language:", read(os.path.join(PLUGIN, "commands", "save-context.md")))


class TestNamedContexts(unittest.TestCase):
    def test_commands_use_named_files(self):
        save = read(os.path.join(PLUGIN, "commands", "save-context.md"))
        resume = read(os.path.join(PLUGIN, "commands", "resume.md"))
        self.assertIn("context-<name>.md", save)
        self.assertIn("do not overwrite", save.lower())
        self.assertIn("context-<name>.md", resume)
        self.assertIn("context-*.md", resume)

    def test_no_stale_single_context_path(self):
        for path in text_files():
            if os.path.basename(path) == "CHANGELOG.md":
                continue
            text = read(path)
            for line in text.splitlines():
                if ".maestro-ai/context.md" in line:
                    self.assertIn("old", line.lower(), "%s: %s" % (path, line))


class TestRelease(unittest.TestCase):
    def test_license_and_resume_fallback(self):
        self.assertIn("MIT License", read(os.path.join(ROOT, "LICENSE")))
        plugin = load_json(os.path.join(PLUGIN, ".claude-plugin", "plugin.json"))
        self.assertEqual(plugin.get("license"), "MIT")
        resume = read(os.path.join(PLUGIN, "commands", "resume.md"))
        self.assertIn("~/Downloads", resume)
        self.assertIn("never copy it", resume)

    def test_common_folder_and_path_line(self):
        save = read(os.path.join(PLUGIN, "commands", "save-context.md"))
        resume = read(os.path.join(PLUGIN, "commands", "resume.md"))
        self.assertIn("~/Documents/maestro-ai/", save)
        self.assertIn("~/Documents/maestro-ai/", resume)
        self.assertIn("Path:", save)
        self.assertIn("Never create a second copy", save)
        self.assertIn("grant access", save)
        self.assertIn("grant access", resume)
        self.assertIn("never an empty code block", save)

    def test_verification_and_files_to_keep(self):
        save = read(os.path.join(PLUGIN, "commands", "save-context.md"))
        resume = read(os.path.join(PLUGIN, "commands", "resume.md"))
        self.assertIn("## Verified vs assumed", save)
        self.assertIn("## Files to keep", save)
        self.assertIn("not as facts", resume)
        self.assertIn("Files to keep", resume)
        self.assertIn("assumed", resume)

    def test_subject_folders_and_files(self):
        save = read(os.path.join(PLUGIN, "commands", "save-context.md"))
        resume = read(os.path.join(PLUGIN, "commands", "resume.md"))
        self.assertIn("~/Documents/maestro-ai/<subject>/context-<name>.md", save)
        self.assertIn("~/Documents/maestro-ai/<subject>/files/", save)
        self.assertIn("never overwriting", save)
        self.assertIn("~/Documents/maestro-ai/*/", resume)

    def test_save_context_closes_with_resume_line(self):
        save = read(os.path.join(PLUGIN, "commands", "save-context.md"))
        self.assertIn("ready-to-paste command", save)


class TestSessionFolders(unittest.TestCase):
    def test_save_and_resume_handle_session_folders(self):
        save = read(os.path.join(PLUGIN, "commands", "save-context.md"))
        resume = read(os.path.join(PLUGIN, "commands", "resume.md"))
        self.assertIn("local-agent-mode-sessions", save)
        self.assertIn("belongs to this session only", save)
        self.assertIn("attach", resume)
        self.assertIn("full path", resume)


class TestNaming(unittest.TestCase):
    def test_no_bare_maestro(self):
        for path in text_files():
            if os.path.basename(path) == "CHANGELOG.md":
                continue
            self.assertIsNone(re.search(r"\bmaestro\b(?!-ai)", read(path), re.I), path)

    def test_referenced_commands_exist(self):
        for path in text_files():
            for cmd in re.findall(r"/maestro-ai:([\w-]+)", read(path)):
                self.assertTrue(
                    os.path.isfile(os.path.join(PLUGIN, "commands", cmd + ".md")), "%s -> %s" % (path, cmd))

    def test_no_old_portuguese_identifiers(self):
        old = r"pesquisador|analista|implementador|testador|especialista|arquiteto|revisor|orquestracao|salvar-contexto|retomar"
        for path in text_files():
            name = os.path.basename(path)
            if name.endswith(".pt-BR.md") or name == "CHANGELOG.md":
                continue
            self.assertIsNone(re.search(old, read(path), re.I), path)


if __name__ == "__main__":
    unittest.main()
