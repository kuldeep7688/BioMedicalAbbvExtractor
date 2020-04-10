import re

class AbbvExtractor:
	"""
	It identifies shortforms from text (standard format of publications).
	For the identified short form it also extracts the long form.
	"""

	def __init__(self, print_lf_suggestions=False, illegal_shortforms=[]):
		self.print_lf_suggestions = print_lf_suggestions
		self.illegal_shortforms = illegal_shortforms

	def identify_abbreviation(self, text):
		"""
		A string between parenthesis with alphanumeric chara with size >= 2 is
		considered as abbreviation.
		Other rules mentioned below:
		# filtering matches
		# humber of words must be <=2
		# atleast one capital letter
			 : params : 
			 	- text : input text string
			 :output :
			 	- list of abbreviations caught and their string indices.
		"""
		shortform_pattern = r"\([\w\-\.\s]{2,}\)"
		all_matches = re.findall(shortform_pattern, text)
		all_matches = list(set(all_matches))
		all_matches = [
		    mat for mat in all_matches if mat not in self.illegal_shortforms
		]
		all_match_indices = []
		for match in all_matches.copy():
			reduced_match = re.sub('[\s0-9\-]+', '', match)
			if len(match.strip().split()) > 2:
				all_matches.remove(match)
			elif 2 > len(reduced_match) or len(reduced_match) > 15:
				all_matches.remove(match)
			elif len(re.findall("[A-Z]+", match)) < 1:
				all_matches.remove(match)
			else:
				start_index = text.find(match)
				all_match_indices.append(
			    	(start_index, start_index + len(match))
				)
		return all_matches, all_match_indices

	def extract_text_parts(self, abbv, abbv_idx, text):
		"""
		This functions extracts out all the possible long forms for the 
		given abbreviation.
			:params:
				- abbv : shortform around which the text has to be extracted
				- abbv_index : (start_index, end_index) for the abbv in text
				- text : the original text
			:output:
				- list of pairs (text, abbv)
		"""
		abbv = abbv[1: -1]
		text_length = min(len(abbv) * 2, len(abbv) + 5)

		text = text[: abbv_idx[0]].strip()
		text = " ".join(text.split()[-1 * text_length:])

		start_text_index = 0
		prev_temp_char = None
		for char_idx, char in enumerate(text):
			if char == " " and prev_temp_char == ',':
				start_text_index = char_idx
			elif char == ' ' and prev_temp_char == '.':
				start_text_index = char_idx
			prev_temp_char = char

		if start_text_index > 0:
			text = "".join(text[start_text_index + 1:]).strip()

		splitted_text = text.split()
		all_possible_long_form = []

		for i in range(1, len(splitted_text) + 1):
			all_possible_long_form.append(" ".join(splitted_text[-i:]))

		return all_possible_long_form

	def find_long_form(self, abbv, text):
		"""
		Given the abbreviation and spliced text, it extracts out the long form.
			:params:
				- abbv : shortform
				- text : spliced text to search in long form
			:Output:
				- long form and its indices in the text
		"""
		# original_text = deepcopy(text)
		abbv = abbv.lower()
		text = text.lower()
		abbv = abbv[1: -1].replace('-','')
		l_idx = len(text.strip()) - 1

		for i in range(len(abbv) - 1, -1, -1):
			text = text[: l_idx + 1]
			curr_char = abbv[i]
			if i != 0 and l_idx > -1:
				while text[l_idx] != curr_char and (l_idx > -1):
					l_idx -= 1
				l_idx -= 1
			elif i == 0 and l_idx > -1:
				if text[l_idx] == " ":
					l_idx -= 1

				if curr_char == text[0]:
					return True

			else:
				if l_idx < 0:
					return False
		return False

	def get_final_pairs(self, text):
		"""
		Given the text generate a list dictionary of all the
		abbreviations and their long forms.

			:params:
				- text : text
			:Output:
				- list of all dictionaries for all the matched found.
		"""
		all_sf_lf_pairs = []
		all_abbvs, all_abbvs_indices = self.identify_abbreviation(text)
		for abbv, abbv_idx in zip(all_abbvs, all_abbvs_indices):
			temp_te_list = self.extract_text_parts(abbv, abbv_idx, text)
			te_list = []
			for te in temp_te_list:
				te_list.append(te)
				if te[0] == '-':
					te_list.append(te[1:])
				elif "-" in te:
					te_list.append(te.split("-")[-1].strip())
				else:
					pass

			if self.print_lf_suggestions:
				print(te_list)

			form_list = [
				(self.find_long_form(abbv, te), te)
				for te in te_list if self.find_long_form(abbv, te) is True
			]
			if len(form_list) > 0:
				lf = form_list[0][1].strip(',')
				if lf[-1] in [',', '.', '/', '*', '!']:
					lf = lf[:-1]

				lf_start_idx = text.find(lf + " (")
				lf_end_idx = lf_start_idx  + len(lf)
				all_sf_lf_pairs.append(
					{
						"abbv": abbv,
						"long_form": lf,
						"lf_start_end_indices": (lf_start_idx, lf_end_idx),
						"abbv_start_end_indices": abbv_idx
					}
				)
			else:
				lf = ""
				lf_start_idx = None
				lf_end_idx = None
				all_sf_lf_pairs.append(
					{
						"abbv": abbv,
						"long_form": lf,
						"lf_start_end_indices": (lf_start_idx, lf_end_idx),
						"abbv_start_end_indices": abbv_idx
					}
				)
		return all_sf_lf_pairs
