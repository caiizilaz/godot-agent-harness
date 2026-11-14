"""Require matching content revisions and executable examples across locales."""
from pathlib import Path
import re
root = Path(__file__).resolve().parents[2]
for topic in ('quickstart', 'migration', 'troubleshooting', 'case-studies'):
    texts = [(root / 'docs' / topic / (locale + '.md')).read_text() for locale in ('th','en','zh-Hans')]
    revisions = [re.search(r'content-revision: (\d+)', text).group(1) for text in texts]
    assert len(set(revisions)) == 1, topic + ': stale translation revision'
    snippets = [re.findall(r'```sh\n(.*?)```', text, re.S) for text in texts]
    assert snippets[0] == snippets[1] == snippets[2], topic + ': command drift'
print('locale parity: 4 topics × 3 languages; revisions and command snippets agree')
