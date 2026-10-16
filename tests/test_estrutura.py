"""Testes de estrutura do repositório: versões em sincronia, agentes, comandos e nome do plugin."""
import glob
import json
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = os.path.join(ROOT, "maestro-ai")


def ler(caminho):
    with open(caminho, encoding="utf-8") as f:
        return f.read()


def frontmatter(caminho):
    texto = ler(caminho)
    m = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
    assert m, "sem frontmatter: " + caminho
    campos = {}
    for linha in m.group(1).splitlines():
        if ":" in linha:
            k, v = linha.split(":", 1)
            campos[k.strip()] = v.strip()
    return campos


class TestEstrutura(unittest.TestCase):
    def test_versoes_em_sincronia(self):
        plugin = json.loads(ler(os.path.join(PLUGIN, ".claude-plugin", "plugin.json")))
        mkt = json.loads(ler(os.path.join(ROOT, ".claude-plugin", "marketplace.json")))
        entrada = next(p for p in mkt["plugins"] if p["name"] == plugin["name"])
        self.assertEqual(plugin["version"], entrada["version"],
                         "suba a versão em plugin.json E marketplace.json ao mesmo tempo")

    def test_changelog_menciona_a_versao_atual(self):
        plugin = json.loads(ler(os.path.join(PLUGIN, ".claude-plugin", "plugin.json")))
        changelog = ler(os.path.join(ROOT, "CHANGELOG.md"))
        self.assertIn("[" + plugin["version"] + "]", changelog, "adicione a versão ao CHANGELOG.md")

    def test_agentes(self):
        arquivos = sorted(glob.glob(os.path.join(PLUGIN, "agents", "*.md")))
        self.assertEqual(len(arquivos), 7)
        for a in arquivos:
            with self.subTest(os.path.basename(a)):
                fm = frontmatter(a)
                for campo in ("name", "description", "model", "tools"):
                    self.assertIn(campo, fm)
                self.assertEqual(fm["name"], os.path.basename(a)[:-3])
                self.assertIn(fm["model"], {"haiku", "sonnet", "opus"})

    def test_arquiteto_roda_em_opus_por_padrao(self):
        # Decisão de projeto: o Fable só entra se o usuário aprovar, nunca por padrão.
        self.assertEqual(frontmatter(os.path.join(PLUGIN, "agents", "arquiteto.md"))["model"], "opus")

    def test_agentes_de_leitura_nao_editam(self):
        for nome in ("pesquisador", "analista", "arquiteto", "revisor"):
            with self.subTest(nome):
                ferramentas = frontmatter(os.path.join(PLUGIN, "agents", nome + ".md"))["tools"]
                for proibida in ("Edit", "Write"):
                    self.assertNotIn(proibida, ferramentas)

    def test_so_o_pesquisador_acessa_a_web(self):
        for a in glob.glob(os.path.join(PLUGIN, "agents", "*.md")):
            nome = os.path.basename(a)[:-3]
            ferramentas = frontmatter(a)["tools"]
            with self.subTest(nome):
                self.assertEqual("WebSearch" in ferramentas or "WebFetch" in ferramentas, nome == "pesquisador")

    def test_comandos_tem_descricao(self):
        for c in glob.glob(os.path.join(PLUGIN, "commands", "*.md")):
            with self.subTest(os.path.basename(c)):
                self.assertIn("description", frontmatter(c))

    def test_skill_tem_nome_e_descricao(self):
        fm = frontmatter(os.path.join(PLUGIN, "skills", "orquestracao", "SKILL.md"))
        self.assertEqual(fm["name"], "orquestracao")
        self.assertTrue(fm["description"])

    def test_hooks_apontam_para_scripts_existentes(self):
        cfg = json.loads(ler(os.path.join(PLUGIN, "hooks", "hooks.json")))
        scripts = set()
        for grupos in cfg["hooks"].values():
            for g in grupos:
                for h in g["hooks"]:
                    scripts.update(re.findall(r"hooks/([\w.-]+\.py)", h["command"]))
        self.assertTrue(scripts)
        for s in scripts:
            self.assertTrue(os.path.isfile(os.path.join(PLUGIN, "hooks", s)), s)

    def test_nome_do_plugin_consistente(self):
        # o nome antigo "maestro" (sem -ai) não deve reaparecer
        antigo = re.compile(r"\bmaestro\b(?!-ai)")
        for raiz, dirs, arquivos in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", "tests"}]
            for f in arquivos:
                if f.endswith((".md", ".json", ".py", ".yml")) and f != "CHANGELOG.md":
                    caminho = os.path.join(raiz, f)
                    with self.subTest(os.path.relpath(caminho, ROOT)):
                        self.assertIsNone(antigo.search(ler(caminho)))


if __name__ == "__main__":
    unittest.main()
