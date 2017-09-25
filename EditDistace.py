import shelve
import operator


class EditDistance(object):
    @staticmethod
    def edit_distance(source_word, target_word):
        max_len = max(len(source_word), len(target_word))
        matrix = [[0 for i in xrange(max_len)] for i in xrange(max_len)]
        for i in xrange(len(source_word)):
            matrix[i][0] = i
        for i in xrange(len(target_word)):
            matrix[0][i] = i
        for i in xrange(len(source_word)):
            for j in xrange(len(target_word)):
                if source_word[i] == target_word[j]:
                    argument1 = matrix[i - 1][j - 1] + 0
                else:
                    argument1 = matrix[i - 1][j - 1] + 1
                matrix[i][j] = min(argument1, matrix[i - 1][j] + 1,
                                   matrix[i][j - 1] + 1)
        return matrix[len(source_word) - 1][len(target_word) - 1]

    def top_corrections(self, source_word):
        edit_distances = []
        qc = shelve.open("query_corpus.db")
        for word in qc.iterkeys():
            edit_distances.append((word, self.edit_distance(source_word,
                                                            word), qc[word]))
        edit_distances.sort(key=operator.itemgetter(1))
        edit_distances = edit_distances[0:5]
        edit_distances.sort(key=operator.itemgetter(2), reverse=True)
        top_corrections = [i[0] for i in edit_distances]
        return top_corrections
