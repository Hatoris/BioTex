



class LatexElements:

    @staticmethod
    def subsubsection(title):
        return r"\subsubsection{" + title + "}"

    @staticmethod
    def item(sentence):
        return r"\item " + sentence

    @staticmethod
    def enumerate(sentences):
        """print a ennumerate list for latex
        
        Parameters
        ----------
        sentences : List
            for each elements in sentences return a new lines
        """
        print(r"\begin{enumerate}")
        for sentence in sentences:
            print(f"\\item {sentence}")
        print(r"\end{enumerate}")
