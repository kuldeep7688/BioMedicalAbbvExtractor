import re
from nltk import sent_tokenize
from utils.abbv_extractor import AbbvExtractor


class TextPreprocessor(AbbvExtractor):
	"""
	A class for preprocessing publications text.
	"""

	def __init__(
		self, remove_html_tags=True, print_lf_suggestions=False,
		add_indicators_to_replaced_lf=False, illegal_shortforms=[]
	):
		# super().__init__(print_lf_suggestions)
		# super().__init__(illegal_shortforms)
		self.print_lf_suggestions = print_lf_suggestions
		self.illegal_shortforms = illegal_shortforms
		self.remove_html_tags_flag = remove_html_tags
		self.html_pattern = re.compile(r'<[\/\W\:]+>')
		self.add_indicators_to_replaced_lf = add_indicators_to_replaced_lf

	def remove_html_tags(self, text):
		"""
		Remove anny html tags present in the text.
		"""
		cleantext = re.sub(self.html_pattern, ' ', text)
		cleantext = re.sub(r'\s{2,}', ' ', cleantext)
		return cleantext

	def small_preprocessing(self, text):
		return re.sub('--', "-", text)

	def get_abbv_lf_pair_dict(self, text):
		return self.get_final_pairs(text)

	def replace_abbv_with_lf(self, text, sf_lf_dict, spacy_sent_tokenizer=None, split_sentences=True):
		for item in sf_lf_dict:
			if len(item['long_form']) > 0:
				# remove the sf (sf) from text
				text = text[:item["abbv_start_end_indices"][0]] + \
						' ' * len(item["abbv"]) + \
						text[item["abbv_start_end_indices"][1]:]

			else:
				text = text[:item["abbv_start_end_indices"][0]] + \
						' ' + item["abbv"][1: -1] +  ' ' +\
						text[item["abbv_start_end_indices"][1]:]

		text = re.sub(r'\s+', ' ', text)
		if split_sentences is True:
			if spacy_sent_tokenizer is None:
				sentences = sent_tokenize(text)
			else:
				sentences = [sent.text for sent in spacy_sent_tokenizer(text.strip()).sents]

			for item in sf_lf_dict:
				sf_pattern = '[\s\.\,\/]' + item["abbv"][1:-1] + "[^S:]"
				if len(item["long_form"]) > 0:
					for i, sentence in enumerate(sentences.copy()):
						try:
							sentence = re.sub(
								sf_pattern, ' ' + item["long_form"] + ' ',
								sentence
							)
						except Exception as e:
							print(e)

						if self.add_indicators_to_replaced_lf:
							sentence = sentence.replace(
								item["long_form"], " LFS:" +
								item["long_form"] + ":LFE "
							)
						sentences[i] = sentence
				else:
					for i, sentence in enumerate(sentences):
						try:
							if self.add_indicators_to_replaced_lf:
								sentence = re.sub(
									sf_pattern, ' LFS:' + item["abbv"][1:-1] +
									':LFE ', sentence
								)
							else:
								sentence = re.sub(
									sf_pattern, item["abbv"][1:-1], sentence
								)

						except Exception as e:
							print(e)
						sentences[i] = sentence

			for i, sentence in enumerate(sentences):
				sentence = re.sub(r'\s{2, }', ' ', sentence)
				sentence = re.sun(r'\s+', ' ', sentence)
				sentence = sentence.strip()
				sentences[i] = sentence
			return sentences
		else:
			for item in sf_lf_dict:
				sf_pattern = "[\s\.\,\/]" + item["abbv"][1:-1] + "[^S:]"
				if len(item["long_form"]) > 0:
					try:
						text = re.sub(
							sf_pattern, ' ' + item["long_form"] + ' ',
							text
						)
					except Exception as e:
						print(e)

					if self.add_indicators_to_replaced_lf:
						text = text.replace(
							item["long_form"], " LFS:" +
							item["long_form"] + ":LFE "
						)
				else:
					try:
						text = re.sub(
							sf_pattern, ' LFS:' + item["abbv"][1:-1] +
									':LFE ', text
						)
					except Exception as e:
						print(e)

			text = re.sub(r'\s{2, }', " ", text)
			text = re.sub(r'\s+', ' ', text)
			return text

	def get_final_text(self, text):
		if self.remove_html_tags_flag:
			text = self.remove_html_tags(text)

		text = self.small_preprocessing(text)
		sf_lf_dict = self.get_abbv_lf_pair_dict(text)
		text = self.replace_abbv_with_lf(
			text, sf_lf_dict,
			split_sentences=False
		)
		return text

	def get_final_sentences(self, text, spacy_sent_tokenizer):
		if self.remove_html_tags_flag:
			text = self.remove_html_tags(text)
		text = self.small_preprocessing(text)
		sf_lf_dict =  self.get_abbv_lf_pair_dict(text)
		sentences = self.replace_abbv_with_lf(
			text, sf_lf_dict,
			split_sentences=True,
			spacy_sent_tokenizer=spacy_sent_tokenizer
		)
		return sentences