import re
from nltk.corpus import stopwords
import nltk


def clean_text(text):
  """Cleans up raw text.

  Args:
    text: A string containing the raw text.

  Returns:
    A string containing the cleaned text.
  """
  tokens = re.split(r'\s+', text)
  tokens = [token.lower() for token in tokens]
  tokens = [re.sub(r'[^\w\s]', '', token) for token in tokens]
  stop_words = set(stopwords.words('english'))
  tokens = [token for token in tokens if token not in stop_words]
  tokens = [nltk.WordNetLemmatizer().lemmatize(token) for token in tokens]
  tokens = [re.sub(r'[^a-zA-Z0-9\s]', '', token) for token in tokens]
  cleaned_text = ' '.join(tokens)
  return cleaned_text

