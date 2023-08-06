import html
import gensim

def tokenize(text):
  s = html.unescape(text)
  s = gensim.utils.simple_preprocess(s)
  return s

stopwords_sets = {
    'english': {"it", "its", "itself", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "of", "at", "by", "for", "with", "to", "from", "in", "then", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"}
}

def analyzeEnglish(text):
  tokens = tokenize(text)
  final_tokens = []
  for token in tokens:
    if token not in stopwords_sets['english']:
      final_tokens.append(token)
  return final_tokens

analyzers = {
  'english': analyzeEnglish
}

def analyze(text, analyzer='english', return_text=False):
    tokens = analyzers[analyzer](text)
    if return_text:
        return ' '.join(tokens)
    else:
        return tokens

def analyze_from_mapping(field, value, mapping, return_text=True):
    spec = mapping
    for f in field.split('.'):
        spec = spec.get('properties', spec)
        spec = spec.get(f, {})
    analyzer_type = spec.get('analyzer', 'english')
    return analyze(value, analyzer=analyzer_type, return_text=return_text)