from gesture2macro.rules import load_rules, Rule


def test_load_rules(tmp_path):
    yaml_content = """
- name: Test
  gesture: PALMA
  macro:
    type: key_combo
    sequence:
      - ctrl+a
  cooldown_ms: 100
"""
    yaml_path = tmp_path / "rules.yaml"
    yaml_path.write_text(yaml_content, encoding="utf-8")
    rules = load_rules(yaml_path)
    assert len(rules) == 1
    rule = rules[0]
    assert isinstance(rule, Rule)
    assert rule.gesture == "PALMA"
    assert rule.macro.type == "key_combo"
