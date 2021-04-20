from __future__ import print_function
import random
import pandas as pd

header = ['temperature', 'humidity', 'lable']
labels = ['Kylrum', 'Klassrum', 'Lärarrum']


def unique_vals(rows, col):
    """Find the unique values for a column in a dataset."""
    return set([row[col] for row in rows])


def class_counts(rows):
    """Counts the number of each type of example in a dataset."""
    counts = {}  # a dictionary of label -> count.
    for row in rows:
        # in our dataset format, the label is always the last column
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts


def is_numeric(value):
    """Test if a value is numeric."""
    return isinstance(value, int) or isinstance(value, float)


class Question:
    """A Question is used to partition a dataset.

    This class just records a 'column number' (e.g., 0 for Color) and a
    'column value' (e.g., Green). The 'match' method is used to compare
    the feature value in an example to the feature value stored in the
    question. See the demo below.
    """

    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        # Compare the feature value in an example to the
        # feature value in this question.
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def moreless(self, val):
        # Compare the feature value in an example to the
        # feature value in this question.
        if is_numeric(val):
            return val >= self.value
        else:
            return val < self.value

    def __repr__(self):
        # This is just a helper method to print
        # the question in a readable format.
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            header[self.column], condition, str(self.value))


def partition(rows, question):
    """Partitions a dataset.

    For each row in the dataset, check if it matches the question. If
    so, add it to 'true rows', otherwise, add it to 'false rows'.
    """
    true_rows, false_rows = [], []
    for row in rows:
        if question.moreless(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows


def partitionMoreless(rows, question):
    """Partitions a dataset.

    For each row in the dataset, check if it matches the question. If
    so, add it to 'true rows', otherwise, add it to 'false rows'.
    """
    true_rows, false_rows = [], []
    for row in rows:
        if question.moreless(row[question.column]):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows


def gini(rows):
    """Calculate the Gini Impurity for a list of rows.

    There are a few different ways to do this, I thought this one was
    the most concise. See:
    https://en.wikipedia.org/wiki/Decision_tree_learning#Gini_impurity
    """
    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity


def info_gain(left, right, current_uncertainty):
    """Information Gain.

    The uncertainty of the starting node, minus the weighted impurity of
    two child nodes.
    """
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)


def find_best_split(rows):
    """Find the best question to ask by iterating over every feature / value
    and calculating the information gain."""
    best_gain = 0  # keep track of the best information gain
    best_question = None  # keep train of the feature / value that produced it
    current_uncertainty = gini(rows)
    n_features = len(rows[0]) - 1  # number of columns

    for col in range(n_features):  # for each feature

        values = set([row[col] for row in rows])  # unique values in the column

        for val in values:  # for each value

            question = Question(col, val)

            # try splitting the dataset
            true_rows, false_rows = partitionMoreless(rows, question)

            # Skip this split if it doesn't divide the
            # dataset.
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            # Calculate the information gain from this split
            gain = info_gain(true_rows, false_rows, current_uncertainty)

            # You actually can use '>' instead of '>=' here
            # but I wanted the tree to look a certain way for our
            # toy dataset.
            if gain >= best_gain:
                best_gain, best_question = gain, question

    return best_gain, best_question


class Leaf:
    """A Leaf node classifies data.

    This holds a dictionary of class (e.g., "Apple") -> number of times
    it appears in the rows from the training data that reach this leaf.
    """

    def __init__(self, rows):
        self.predictions = class_counts(rows)


class Decision_Node:
    """A Decision Node asks a question.

    This holds a reference to the question, and to the two child nodes.
    """

    def __init__(self,
                 question,
                 true_branch,
                 false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch


def build_tree(rows):
    """Builds the tree.

    Rules of recursion: 1) Believe that it works. 2) Start by checking
    for the base case (no further information gain). 3) Prepare for
    giant stack traces.
    """

    # Try partitioing the dataset on each of the unique attribute,
    # calculate the information gain,
    # and return the question that produces the highest gain.
    gain, question = find_best_split(rows)

    # Base case: no further info gain
    # Since we can ask no further questions,
    # we'll return a leaf.
    if gain == 0:
        return Leaf(rows)

    # If we reach here, we have found a useful feature / value
    # to partition on.
    true_rows, false_rows = partitionMoreless(rows, question)

    # Recursively build the true branch.
    true_branch = build_tree(true_rows)

    # Recursively build the false branch.
    false_branch = build_tree(false_rows)

    # Return a Question node.
    # This records the best feature / value to ask at this point,
    # as well as the branches to follow
    # dependingo on the answer.
    return Decision_Node(question, true_branch, false_branch)


def print_tree(node, spacing=""):
    """World's most elegant tree printing function."""

    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        print(spacing + "Predict", node.predictions)
        return

    # Print the question at this node
    print(spacing + str(node.question))

    # Call this function recursively on the true branch
    print(spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")

    # Call this function recursively on the false branch
    print(spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")


def classify(row, node):
    """See the 'rules of recursion' above."""

    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        return node.predictions

    # Decide whether to follow the true-branch or the false-branch.
    # Compare the feature / value stored in the node,
    # to the example we're considering.
    if node.question.moreless(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)


def print_leaf(counts):
    """A nicer way to print the predictions at a leaf."""
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs


def createValues():
    values = []
    rules = [
        {'label': 'Kylrum', 'minTemp': 5, 'maxTemp': 9, 'minHum': 22, 'maxHum': 70},
        {'label': 'Klassrum', 'minTemp': 18,
            'maxTemp': 22, 'minHum': 44, 'maxHum': 85},
        {'label': 'Lärarrum', 'minTemp': 20,
            'maxTemp': 25, 'minHum': 50, 'maxHum': 90},
    ]

    for rule in rules:
        times = random.randint(30, 100)
        for i in range(0, times):
            newTemp = round(random.uniform(
                rule['minTemp'], rule['maxTemp']), 1)
            newHum = round(random.uniform(rule['minHum'], rule['maxHum']), 1)
            values.append([newTemp, newHum, rule['label']])

    return values


newValues = createValues()
values = pd.DataFrame(newValues)


def splitData(inputdata, n_trees, ownvalue):
    subsets = []
    split1 = inputdata.sample(frac=0.5, random_state=200)
    split2 = inputdata.drop(split1.index)
    if n_trees != 1:
        feedback1 = splitData(split1, n_trees-1, ownvalue+'a')
        feedback2 = splitData(split2, n_trees-1, ownvalue+'b')
        for i in range(0, len(feedback1)):
            subsets.append(feedback1[i])
            subsets.append(feedback2[i])
    else:
        return [split1, split2]
    return subsets


Subsets = splitData(values, 4, 'a')

print('Antal subsets:', len(Subsets))
print('Antal värden:', len(Subsets[0]))
print(Subsets[0])

my_trees = []
i = 1

for my_set in Subsets:
    my_list = my_set.values.tolist()
    print('Träd', i)
    i += 1
    tree = build_tree(my_list)
    my_trees.append(tree)
    print_tree(tree)


def predictionCounter(row, trees, lable):
    length = len(labels)
    predictions = [0 for i in range(length)]
    for tree in trees:
        prediction = classify(row, tree)

        for i in range(length):
            if prediction.get(labels[i]) is not None:
                predictions[i] += 1
        print("Actual: %s. Predicted: %s" %
              (row[-1], print_leaf(classify(row, tree))))
    return predictions


def randomForest(trees, data):
    for row in data:
        labels = ['Kylrum', 'Lärarrum', 'Klassrum']
        predictions = predictionCounter(row, trees, labels)
        high = max(predictions)
        print("Actual:", row[2], labels[predictions.index(
            high)], ":", max(predictions), "/", len(trees))


print(randomForest(my_trees, values))
