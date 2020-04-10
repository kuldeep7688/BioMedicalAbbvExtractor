from config import ILLEGAL_SHORTFORMS
import re
from pprint import pprint
from utils.utilities import TextPreprocessor


if __name__ == "__main__":
	TP = TextPreprocessor(
	    remove_html_tags=True, print_lf_suggestions=True,
	    add_indicators_to_replaced_lf=True, illegal_shortforms=IILEGAL_SHORTFORMS
	)
	text = "In addition to the SARS coronavirus (treated separately elsewhere in this volume), the complete genome sequences of six species in the coronavirus genus of the coronavirus family [avian infectious bronchitis virus-Beaudette strain (IBV-Beaudette), bovine coronavirus-ENT strain (BCoV-ENT), human coronavirus-229E strain (HCoV-229E), murine hepatitis virus-A59 strain (MHV-A59), porcine transmissible gastroenteritis-Purdue 115 strain (TGEV-Purdue 115), and porcine epidemic diarrhea virus-CV777 strain (PEDV-CV777)] have now been reported. Their lengths range from 27,317 nt for HCoV-229E to 31,357 nt for the murine hepatitis virus-A59, establishing the coronavirus genome as the largest known among RNA viruses. The basic organization of the coronavirus genome is shared with other members of the Nidovirus order (the torovirus genus, also in the family Coronaviridae, and members of the family Arteriviridae) in that the nonstructural proteins involved in proteolytic processing, genome replication, and subgenomic mRNA synthesis (transcription) (an estimated 14-16 end products for coronaviruses) are encoded within the 5'-proximal two-thirds of the genome on gene 1 and the (mostly) structural proteins are encoded within the 3'-proximal one-third of the genome (8-9 genes for coronaviruses). Genes for the major structural proteins in all coronaviruses occur in the 5' to 3' order as S, E, M, and N. The precise strategy used by coronaviruses for genome replication is not yet known, but many features have been established. This chapter focuses on some of the known features and presents some current questions regarding genome replication strategy, the cis-acting elements necessary for genome replication [as inferred from defective interfering (DI) RNA molecules], the minimum sequence requirements for autonomous replication of an RNA replicon, and the importance of gene order in genome replication."
	print(text)
	text2 = TP.get_final_text(text)
	print("Replaced text is : {}".format(text2))

	print("All the extracted short forms and their corresponding long forms are mentioned below:")
	pprint(TP.get_final_pairs(text))
